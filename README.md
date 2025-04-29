# Universidade Estadual do Norte do Paraná

## Alunos
- Gabriel Vilar  
- Joana Shizu  
- Melissa Francielle

## Disciplina
**Computação Gráfica – 4º ano de Ciência da Computação**

## Título do Trabalho
**Contador de Moedas e Objetos por Visão Computacional**

## Descrição do Trabalho
Este trabalho foi desenvolvido como parte da disciplina de Computação Gráfica. O objetivo da atividade foi descrever e implementar um protocolo de visão computacional para contagem de objetos em uma imagem estática. A atividade foi proposta em sala de aula e realizada em grupo, mas cada integrante deve entregar sua versão do documento.

## Descrição do Problema
> "Descrever o protocolo de visão computacional proposto em sala de aula para contagem de objetos. O trabalho pode ser feito em grupo mas todos os integrantes devem entregar o documento."

## Solução Proposta
O sistema utiliza técnicas básicas de segmentação de imagem com processamento em tons de cinza e binarização, aplicando uma busca em largura (BFS) para identificar regiões conectadas (clusters) de pixels que representam possíveis objetos. Após a detecção, as regiões são agrupadas com base na proximidade das suas **bounding boxes**, a fim de evitar contagem duplicada de objetos que estejam muito próximos.

### Estratégias utilizadas:
- Conversão da imagem original para tons de cinza.
- Binarização com limiar fixo.
- Segmentação por BFS para encontrar regiões conectadas.
- Filtragem de clusters pequenos (ruído).
- Agrupamento por proximidade de bounding boxes.
- Exibição visual das detecções com retângulos sobre os objetos.

## Código-Fonte

```python
from PIL import Image, ImageDraw
from collections import deque
import argparse

def get_bbox(cluster):
    xs = [p[0] for p in cluster]
    ys = [p[1] for p in cluster]
    return min(xs), min(ys), max(xs), max(ys)

def bboxes_are_close(bbox1, bbox2, margin=5):
    x1_min, y1_min, x1_max, y1_max = bbox1

```
[Clique aqui para visualizar o código no GitHub](https://github.com/Melissa-Francielle/Object_counter/blob/main/Counter.py)
