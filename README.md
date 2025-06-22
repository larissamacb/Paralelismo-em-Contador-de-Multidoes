<h1>Relatório: Contagem Paralelizada de Pessoas em Imagens com YOLOv5</h1>
Trabalho por Larissa Batista Maciel (@larissamacb) e Samuel Gonçalves de Araujo (@SamuelGdA).
<hr>
<h2>Introdução</h2>
<p>Este projeto consiste em um experimento prático de processamento de imagens e paralelismo aplicado à contagem automática de pessoas. A partir de uma única imagem contendo diversas pessoas, utilizamos a técnica de reconhecimento de cabeças com o modelo YOLOv5 para identificar e contar quantas pessoas estão presentes.</p>
<p>Para simular uma carga computacional significativa, multiplicamos essa imagem inicial, criando um conjunto de 988 cópias idênticas. Em seguida, desenvolvemos um código para paralelizar o processamento dessas imagens, dividindo-as em grupos (“chunks”) e utilizando o módulo multiprocessing do Python para executar a contagem simultaneamente em diferentes números de processos.</p>
<p></p>O objetivo principal do experimento é comparar o desempenho do sistema ao utilizar 1, 2, 4, 6, 8, 12 e 16 processos, avaliando métricas fundamentais como tempo de execução, speedup e eficiência. Essa análise permite entender melhor os ganhos e limitações do paralelismo na tarefa de reconhecimento e contagem em imagens, demonstrando a aplicação prática de conceitos de computação paralela para otimização de tarefas computacionalmente intensivas.</p>

<strong>Configurações da Máquina Utilizada:</strong><br>
Processador: Intel(R) Core(TM) i7-12700 2.10GHz<br>
RAM: 16GB
<hr>
<h2>Descrição do problema</h2>
<p>A contagem automática de pessoas em imagens é uma tarefa importante em diversas áreas, como monitoramento de segurança, análise de fluxo em eventos e estudos urbanos. No entanto, mesmo com modelos avançados de reconhecimento, como o YOLOv5, o processamento de grandes volumes de imagens pode se tornar um gargalo devido ao tempo computacional necessário.</p>

<p>O problema central deste trabalho é otimizar o processamento em lote de um grande número de imagens idênticas para que a contagem de pessoas possa ser realizada de forma mais rápida e eficiente. A estratégia adotada envolve o uso do paralelismo, dividindo a tarefa em partes menores para serem executadas simultaneamente em múltiplos núcleos de processamento.</p>

<p>Esse cenário traz o desafio de avaliar como a divisão do trabalho e a quantidade de processos impactam o desempenho, buscando um equilíbrio entre o ganho de velocidade e o uso eficiente dos recursos computacionais disponíveis.</p>
<hr>
<h2>Solução</h2>
<p>A princípio, testamos a detecção da quantidade de pessoas por meio de um modelo com a finalidade de reconhecer pessoas. Percebemos, então, que em imagens com multidões, como em protestos (que foi o exemplo utilizado), geralmente não há visibilidade de parte suficiente do corpo para que ocorra a identificação. Isso levou ao uso de reconhecimento de cabeças como alternativa, que gerou melhores resultados, embora aquelas que estivessem a uma distância maior da imagem não fossem detectadas. Isso traz a necessidade de um modelo treinado mais especificamente para reconhecer cabeças no contexto de imagens aéreas, nas quais há muito menos características do objeto de detecção que facilitem o reconhecimento, mas não houve um aprofundamento nessa parte pela falta de um fácil acesso a esse modelo específico e porque não é esse o objetivo principal do projeto.</p>
<p>Tendo sido feita uma aproximação satisfatória dos resultados esperados com o teste da imagem representada na figura abaixo, a multiplicamos até o total de 988 imagens idênticas e utilizamos o módulo multiprocessing do Python para dividi-las em chunks, que seriam processados paralelamente pelos núcleos nas quantidades 1, 2, 4, 6, 8, 12 e 16. Testamos cada uma delas e anotamos os resultados de tempo decorrido de processamento para cada caso, assim como calculamos o speedup e a eficiência para fins de comparação. Cada processo foi responsável por carregar e processar um subconjunto das imagens, executando o modelo YOLOv5 para realizar a detecção de cabeças.</p>
<img src=multidao.png>
<hr>
<h2>Resultados</h2>
<p>Com o conjunto de 988 imagens replicadas, foram realizados testes variando a quantidade de processos utilizados para a execução paralela da contagem. A tabela abaixo apresenta os tempos de execução, speedup e eficiência para cada configuração testada:</p>
<br>
<table border="1" cellspacing="0" cellpadding="5">
  <thead>
    <tr>
      <th>Nº de Processos</th>
      <th>Tempo (s)</th>
      <th>SpeedUp</th>
      <th>Eficiência (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>219</td>
      <td>1,00</td>
      <td>100</td>
    </tr>
    <tr>
      <td>2</td>
      <td>156</td>
      <td>1,40</td>
      <td>70</td>
    </tr>
    <tr>
      <td>4</td>
      <td>138</td>
      <td>1,59</td>
      <td>40</td>
    </tr>
    <tr>
      <td>6</td>
      <td>106</td>
      <td>2,06</td>
      <td>34</td>
    </tr>
    <tr>
      <td>8</td>
      <td>114</td>
      <td>1,92</td>
      <td>24</td>
    </tr>
    <tr>
      <td>12</td>
      <td>129</td>
      <td>1,70</td>
      <td>14</td>
    </tr>
    <tr>
      <td>16</td>
      <td>142</td>
      <td>1,54</td>
      <td>10</td>
    </tr>
  </tbody>
</table>
<br>
<p>Para melhor visualização dos resultados, esses números podem ser representados em gráficos:</p>
<img src=graficos.png>
<br>
<p>No primeiro gráfico, o melhor desempenho é representado pelo ponto mais baixo, indicando o menor tempo em que se obtiveram todos os resultados das análises. Diretamente relacionado com o tempo está o speedup, cujo gráfico (segunda imagem) apresenta-se muito semelhante ao que seria o de tempo se estivesse invertido verticalmente. Isso acontece porque ele verifica quão mais rápido foi o processamento em comparação com o caso sequencial. Já a eficiência (terceira imagem) indica quanto do desempenho teórico máximo foi obtido. Esse último foi caracterizado por uma grande queda seguida de outras menores.</p>
<p>Observa-se que o melhor desempenho foi obtido com 6 processos, atingindo um speedup de 2,06, com tempo de execução reduzido em mais de 50% em comparação com a execução sequencial. Porém, a partir de 8 processos, os tempos passam a aumentar progressivamente, indicando perda de desempenho.</p>
<p>As possíveis causas para esse comportamento são relacionados à eficiência e incluem:</p>

<ul>
  <li><strong>Sobrecarga de gerenciamento de processos:</strong> À medida que mais processos são criados, o sistema precisa dedicar mais tempo para coordená-los, o que pode consumir parte do ganho obtido com a paralelização.</li>
  <li><strong>Concorrência de acesso ao disco:</strong> O uso simultâneo de múltiplos processos para carregar imagens pode gerar gargalos no subsistema de I/O.</li>
  <li><strong>Custo de comunicação e sincronização:</strong> O tempo gasto na coordenação entre os processos, especialmente para unir os resultados, pode superar os benefícios da execução paralela quando muitos processos são utilizados.</li>
</ul>

<p>Além dessas causas, é importante considerar a arquitetura da CPU utilizada nos testes. O processador Intel Core i7-12700 possui 12 núcleos físicos (8 de alta performance e 4 de alta eficiência), totalizando 20 threads com Hyper-Threading. O pico de performance ocorreu com 6 processos (speedup de 2,06), mesmo havendo núcleos disponíveis, o que indica que adicionar mais processos não trouxe benefícios — ao contrário, causou queda na eficiência. Isso pode estar relacionado ao uso dos núcleos de eficiência, que são menos potentes, além da contenção de recursos como cache e memória. Também é relevante notar que o Hyper-Threading não apresentou ganhos expressivos nesse tipo de carga computacional intensiva, como a execução do YOLOv5, que tende a se beneficiar mais de núcleos físicos do que de threads lógicas.</p>
<hr>
<h2>Conclusão</h2>
<p>A paralelização do processamento de imagens com o modelo YOLOv5 demonstrou ganhos significativos de desempenho até um certo ponto. O uso de 6 processos apresentou o melhor equilíbrio entre tempo de execução e eficiência computacional, atingindo uma redução expressiva no tempo total necessário para a contagem.</p>
<p>Por outro lado, o experimento evidenciou as limitações da paralelização excessiva, uma vez que o uso de mais processos não resultou em melhores tempos. Pelo contrário, a partir de 8 processos houve degradação do desempenho, causada principalmente pela sobrecarga de gerenciamento, disputa por recursos e limitações do hardware.</p>
<p>Com isso, conclui-se que, para aplicações semelhantes de processamento intensivo com grande volume de dados, a análise prévia da capacidade da máquina e testes empíricos são fundamentais para definir o ponto ótimo de paralelização. O projeto demonstra com clareza a importância do balanceamento entre recursos computacionais e desempenho na aplicação de técnicas de paralelismo em tarefas do mundo real.</p>

