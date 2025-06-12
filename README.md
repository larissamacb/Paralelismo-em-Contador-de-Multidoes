Contagem Paralelizada de Pessoas em Imagens com YOLOv5

Introdução
Este projeto consiste em um experimento prático de processamento de imagens e paralelismo aplicado à contagem automática de pessoas. A partir de uma única imagem contendo diversas pessoas, utilizamos a técnica de reconhecimento de cabeças com o modelo YOLOv5 para identificar e contar quantas pessoas estão presentes.

Para simular uma carga computacional significativa, multiplicamos essa imagem inicial, criando um conjunto de 988 cópias idênticas. Em seguida, desenvolvemos um código para paralelizar o processamento dessas imagens, dividindo-as em grupos (“chunks”) e utilizando o módulo multiprocessing do Python para executar a contagem simultaneamente em diferentes números de processos.

O objetivo principal do experimento é comparar o desempenho do sistema ao utilizar 1, 2, 4, 8 e 16 processos, avaliando métricas fundamentais como tempo de execução, speedup e eficiência. Essa análise permite entender melhor os ganhos e limitações do paralelismo na tarefa de reconhecimento e contagem em imagens, demonstrando a aplicação prática de conceitos de computação paralela para otimização de tarefas computacionalmente intensivas.

Descrição do problema
A contagem automática de pessoas em imagens é uma tarefa importante em diversas áreas, como monitoramento de segurança, análise de fluxo em eventos e estudos urbanos. No entanto, mesmo com modelos avançados de reconhecimento, como o YOLOv5, o processamento de grandes volumes de imagens pode se tornar um gargalo devido ao tempo computacional necessário.

O problema central deste trabalho é otimizar o processamento em lote de um grande número de imagens idênticas para que a contagem de pessoas possa ser realizada de forma mais rápida e eficiente. A estratégia adotada envolve o uso do paralelismo, dividindo a tarefa em partes menores para serem executadas simultaneamente em múltiplos núcleos de processamento.

Esse cenário traz o desafio de avaliar como a divisão do trabalho e a quantidade de processos impactam o desempenho, buscando um equilíbrio entre o ganho de velocidade e o uso eficiente dos recursos computacionais disponíveis.

Solução
A princípio, testamos a detecção da quantidade de pessoas por meio de um modelo com a finalidade de reconhecer pessoas. Percebemos, então, que em imagens com multidões, como em protestos (que foi o exemplo utilizado), geralmente não há visibilidade de parte suficiente do corpo para que ocorra a identificação. Isso levou ao uso de reconhecimento de cabeças como alternativa, que gerou melhores resultados, embora aquelas que estivessem a uma distância maior da imagem não fossem detectadas. Isso traz a necessidade de um modelo treinado mais especificamente para reconhecer cabeças no contexto de imagens aéreas, nas quais há muito menos características do objeto de detecção que facilitem o reconhecimento, mas não houve um aprofundamento nessa parte pela falta de um fácil acesso a esse modelo específico e porque não é esse o objetivo principal do projeto.

Tendo sido feita uma aproximação satisfatória dos resultados esperados com o teste da imagem representada na figura X, a multiplicamos até o total de 988 imagens idênticas. Falar do processamento

Resultados

Conclusão