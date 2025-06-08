import argparse
import os
import shutil
import time
from multiprocessing import Process
from pathlib import Path


def run_detect_on_dir(weights, source, classes, additional_args):
    command = f"python detect_single.py --weights {weights} --source {source} --classes {' '.join(map(str, classes))} {additional_args}"
    os.system(command)

def split_images(source_folder, num_parts):
    image_paths = list(Path(source_folder).glob("*.png"))
    total_images = len(image_paths)
    
    if total_images == 0:
        raise ValueError(f"Nenhuma imagem encontrada em {source_folder}")
    
    # Evita num_parts > total_images para não gerar chunk_size = 0
    num_parts = min(num_parts, total_images)
    
    # Calcula chunk_size, agora sempre >= 1
    chunk_size = (total_images + num_parts - 1) // num_parts
    
    chunks = [image_paths[i:i + chunk_size] for i in range(0, total_images, chunk_size)]
    return chunks



def prepare_dirs(chunks, base_temp_dir):
    temp_dirs = []
    for i, chunk in enumerate(chunks):
        temp_dir = base_temp_dir / f"proc_{i}"
        img_dir = temp_dir / "img_set"
        img_dir.mkdir(parents=True, exist_ok=True)
        for img_path in chunk:
            shutil.copy(img_path, img_dir / img_path.name)
        temp_dirs.append(temp_dir)
    return temp_dirs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, required=True)
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--classes', nargs='+', type=int, required=True)
    parser.add_argument('--img-size', type=int, default=640)
    parser.add_argument('--conf-thres', type=float, default=0.25)
    parser.add_argument('--iou-thres', type=float, default=0.45)
    parser.add_argument('--device', default='')
    parser.add_argument('--view-img', action='store_true')
    parser.add_argument('--save-txt', action='store_true')
    parser.add_argument('--save-conf', action='store_true')
    parser.add_argument('--augment', action='store_true')
    parser.add_argument('--agnostic-nms', action='store_true')
    parser.add_argument('--project', default='runs/detect')
    parser.add_argument('--name', default='exp')
    parser.add_argument('--exist-ok', action='store_true')
    opt = parser.parse_args()

    source = Path(opt.source)
    weights = opt.weights
    classes = opt.classes

    additional_args = []
    for k, v in vars(opt).items():
        if k not in ['weights', 'source', 'classes'] and v:
            if isinstance(v, bool):
                additional_args.append(f"--{k}")
            else:
                additional_args.append(f"--{k} {v}")
    additional_args = ' '.join(additional_args)

    for num_proc in [1]:
        print(f"\nRunning with {num_proc} parallel processes...")
        chunks = split_images(source, num_proc)
        base_temp_dir = Path("yolo_parallel_temp")
        if base_temp_dir.exists():
            shutil.rmtree(base_temp_dir)
        temp_dirs = prepare_dirs(chunks, base_temp_dir)

        procs = []
        t_start = time.time()
        for temp_dir in temp_dirs:
            p = Process(target=run_detect_on_dir, args=(weights, str(temp_dir / "img_set"), classes, additional_args))
            p.start()
            procs.append(p)

        for p in procs:
            p.join()

        print(f"Completed in {time.time() - t_start:.2f} seconds.")


if __name__ == '__main__':
    main()