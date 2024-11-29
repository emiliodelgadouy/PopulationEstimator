import processing
import os

crs = QgsProject.instance().crs().authid()

# Eliminar la capa 'grid' si ya existe en el proyecto
for layer in QgsProject.instance().mapLayers().values():
    if layer.name() == "grid":
        QgsProject.instance().removeMapLayers([layer.id()])

# Paso 1: Definir la coordenada central
x_center = 576331  # Reemplaza con tu coordenada X
y_center = 6137979  # Reemplaza con tu coordenada Y

# Paso 2: Definir la extensión alrededor del punto central
grid_width = 50000  # Ancho total de la cuadrícula (en metros)
grid_height = 50000  # Alto total de la cuadrícula (en metros)

xmin = x_center - (grid_width / 2)
xmax = x_center + (grid_width / 2)
ymin = y_center - (grid_height / 2)
ymax = y_center + (grid_height / 2)

# Paso 3: Establecer el CRS
# crs = QgsCoordinateReferenceSystem('EPSG:32721')  # Reemplaza con tu código EPSG

# Paso 4: Crear la cuadrícula y especificar la ruta de salida
ruta_salida = '/opt/projects/marvik/grid.shp'  # Especifica la ruta donde deseas guardar la capa

grid = processing.run("native:creategrid", {
    'TYPE': 2,
    'EXTENT': f'{xmin},{xmax},{ymin},{ymax}',
    'HSPACING': 500,
    'VSPACING': 500,
    'HOVERLAY': 0,
    'VOVERLAY': 0,
    'CRS': crs,
    'OUTPUT': ruta_salida  # Guardar la capa en un archivo permanente
})

# Paso 5: Cargar la capa desde el archivo guardado
grid_layer = QgsVectorLayer(ruta_salida, 'grid', 'ogr')
if not grid_layer.isValid():
    print("La capa no se pudo cargar.")
else:
    QgsProject.instance().addMapLayer(grid_layer)

# Paso 6: Ajustar la simbología para contorno sin relleno
symbol = QgsFillSymbol.createSimple({
    'color': '0,0,0,0',             # Sin relleno (transparente)
    'outline_color': '255,0,0,255', # Color del contorno (rojo)
    'outline_width': '0.26',        # Ancho del contorno en milímetros
    'style': 'no'                   # Sin estilo de relleno
})

# Asignar el símbolo a la capa
grid_layer.renderer().setSymbol(symbol)
grid_layer.triggerRepaint()
