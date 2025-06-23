import argparse
import sys
from pathlib import Path

import torch
from models.common import DetectMultiBackend
from utils.datasets import LoadImages
from utils.general import (check_img_size, non_max_suppression, scale_boxes,
                           xyxy2xywh, set_logging, increment_path)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device, time_sync


def run(weights, source, classes, img_size=640, conf_thres=0.25, iou_thres=0.45, device=''):
    set_logging()
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=False)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(img_size, stride)

    dataset = LoadImages(source, img_size=imgsz, stride=stride)


    model.warmup(imgsz=(1 if pt else 1, 3, imgsz, imgsz))

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255  # normalize to 0-1
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=False)

        for i, det in enumerate(pred):
            im0 = im0s.copy()
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()
                # Aqui você pode salvar resultados, printar, etc.
                print(f'{path}: {len(det)} objetos detectados')

    print('Detecção concluída para:', source)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, required=True, help='caminho do arquivo de pesos')
    parser.add_argument('--source', type=str, required=True, help='arquivo ou pasta de imagens')
    parser.add_argument('--classes', nargs='+', type=int, required=True, help='classes para detectar')
    parser.add_argument('--img-size', type=int, default=640, help='tamanho da imagem')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confiança mínima')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='limite IOU')
    parser.add_argument('--device', default='', help='dispositivo (cpu ou cuda)')
    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    run(opt.weights, opt.source, opt.classes, opt.img_size, opt.conf_thres, opt.iou_thres, opt.device)
