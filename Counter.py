from PIL import Image, ImageDraw
from collections import deque
import argparse

def get_bbox(cluster):
    xs = [p[0] for p in cluster]
    ys = [p[1] for p in cluster]
    return min(xs), min(ys), max(xs), max(ys)

def bboxes_are_close(bbox1, bbox2, margin=5):
    # Verifica se as bounding boxes estão próximas
    x1_min, y1_min, x1_max, y1_max = bbox1
    x2_min, y2_min, x2_max, y2_max = bbox2
    return not (
        x1_max + margin < x2_min or
        x2_max + margin < x1_min or
        y1_max + margin < y2_min or
        y2_max + margin < y1_min
    )

# Argumento da imagem
parser = argparse.ArgumentParser(description='Segmentação de imagem')
parser.add_argument('filename', type=str, help='Nome do arquivo de imagem')
args = parser.parse_args()

# Carregar imagem e converter para escala de cinza
image = Image.open(args.filename)
gray_image = image.convert('L')

# Limiar para binarização
threshold = 160
binary_image = gray_image.point(lambda pixel: 0 if pixel < threshold else 255)
visited = Image.new('1', binary_image.size)
clusters = []
neighborhood = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# BFS para encontrar clusters
for x in range(binary_image.width):
    for y in range(binary_image.height):
        if visited.getpixel((x, y)) == 0 and binary_image.getpixel((x, y)) == 0:
            queue = deque([(x, y)])
            cluster = []

            while queue:
                current_x, current_y = queue.popleft()
                if visited.getpixel((current_x, current_y)) == 0 and binary_image.getpixel((current_x, current_y)) == 0:
                    visited.putpixel((current_x, current_y), 1)
                    cluster.append((current_x, current_y))
                    for dx, dy in neighborhood:
                        new_x = current_x + dx
                        new_y = current_y + dy
                        if 0 <= new_x < binary_image.width and 0 <= new_y < binary_image.height:
                            queue.append((new_x, new_y))

            if len(cluster) > 2000:
                clusters.append(cluster)

# Agrupar clusters com base em bounding boxes próximas
merged_clusters = []
bboxes = []

for cluster in clusters:
    bbox = get_bbox(cluster)
    merged = False
    for i, other_bbox in enumerate(bboxes):
        if bboxes_are_close(bbox, other_bbox):
            merged_clusters[i].extend(cluster)
            # Atualizar a bbox
            bboxes[i] = get_bbox(merged_clusters[i])
            merged = True
            break
    if not merged:
        merged_clusters.append(cluster)
        bboxes.append(bbox)

# Visualizar resultado
result = image.copy()
draw = ImageDraw.Draw(result)

for bbox in bboxes:
    draw.rectangle(bbox, outline=(255, 0, 0), width=2)

print('Número de objetos detectados:', len(merged_clusters))
result.show()
