import processing
from qgis.core import QgsProject, QgsFillSymbol, QgsField, edit, QgsVectorLayer
from PyQt5.QtCore import QVariant
import os

# Eliminar la capa 'grid_montevideo' si ya existe en el proyecto
for layer in QgsProject.instance().mapLayers().values():
    if layer.name() == "grid_montevideo":
        QgsProject.instance().removeMapLayers([layer.id()])

# Obtener las capas necesarias
grid_layer = QgsProject.instance().mapLayersByName("grid")[0]
montevideo_layer = QgsProject.instance().mapLayersByName('v_sig_departamentos')[0]

# Especificar la ruta de salida para la capa permanente
ruta_salida = '/opt/projects/marvik/grid_montevideo.shp'  # Reemplaza con tu ruta deseada

# Asegurarse de que el archivo no exista previamente
if os.path.exists(ruta_salida):
    os.remove(ruta_salida)

# Ejecutar el proceso de extracción y guardar en la ruta especificada
extract_result = processing.run("native:extractbylocation", {
    'INPUT': grid_layer,
    'PREDICATE': [0],  # Intersecta
    'INTERSECT': montevideo_layer,
    'OUTPUT': ruta_salida  # Guardar en archivo permanente
})

# Cargar la capa desde el archivo guardado
extracted_grid = QgsVectorLayer(ruta_salida, 'grid_montevideo', 'ogr')
if not extracted_grid.isValid():
    print("La capa no se pudo cargar.")
else:
    # Ajustar la simbología para contorno sin relleno
    symbol = QgsFillSymbol.createSimple({
        'color': '0,0,0,0',
        'outline_color': '255,0,0,255',
        'outline_width': '0.26'
    })
    extracted_grid.renderer().setSymbol(symbol)

    # Añadir el campo 'id' y actualizar los valores
    extracted_grid.dataProvider().addAttributes([QgsField("id", QVariant.Int)])
    extracted_grid.updateFields()

    with edit(extracted_grid):
        for i, feature in enumerate(extracted_grid.getFeatures(), start=1):
            feature['id'] = i
            extracted_grid.updateFeature(feature)

    # Guardar los cambios en el archivo
    extracted_grid.commitChanges()

    # Añadir la capa al proyecto
    QgsProject.instance().addMapLayer(extracted_grid)
