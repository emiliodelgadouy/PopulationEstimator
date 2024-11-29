print("Iniciando el proceso de exportación de imágenes...")

import os
from qgis.utils import iface
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtGui import QImage, QPainter, QColor
from qgis.core import (
    QgsProject,
    QgsMapSettings,
    QgsMapRendererCustomPainterJob,
    QgsRectangle,
    QgsCoordinateReferenceSystem
)

# Configuración inicial
output_folder = '/opt/projects/marvik/fotos'
os.makedirs(output_folder, exist_ok=True)

project = QgsProject.instance()
crs = project.crs()
print(f"Utilizando CRS: {crs.authid()}")

# Obtener la capa de cuadrícula
grid_layers = project.mapLayersByName('grid_montevideo')
if not grid_layers:
    print("La capa 'grid_montevideo' no se encontró.")
    exit()
grid_layer = grid_layers[0]
print(f"Capa de cuadrícula: {grid_layer.name()}")

# Obtener las capas visibles y excluir la cuadrícula
root = project.layerTreeRoot()
visible_layers = [
    layer.layer() for layer in root.findLayers()
    if layer.isVisible() and layer.layer() != grid_layer
]


# Configuración de renderización que es constante
map_settings = QgsMapSettings()
map_settings.setLayers(visible_layers)
map_settings.setBackgroundColor(QColor(255, 255, 255))
map_settings.setOutputSize(QSize(500, 500))
map_settings.setRotation(0)
map_settings.setDestinationCrs(crs)

# Preparar variables constantes
image_size = map_settings.outputSize()
transparent_color = QColor(255, 255, 255, 0)

# Iterar sobre cada celda
for feature in grid_layer.getFeatures():
    # Obtener la extensión de la geometría
    extent = feature.geometry().boundingBox()

    # Actualizar la extensión en map_settings
    map_settings.setExtent(extent)

    # Renderizar el mapa
    image = QImage(image_size.width(), image_size.height(), QImage.Format_ARGB32_Premultiplied)
    image.fill(transparent_color)
    painter = QPainter(image)
    job = QgsMapRendererCustomPainterJob(map_settings, painter)
    job.start()
    job.waitForFinished()
    painter.end()

    # Usar el ID de la feature para el nombre del archivo
    filename = f'{feature["id"]}.png'  # Asegúrate de que el campo 'id' existe
    output_path = os.path.join(output_folder, filename)

    # Guardar la imagen
    image.save(output_path, 'png')

    print(f'Imagen guardada: {output_path}')

print("Proceso completado.")
