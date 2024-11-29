from qgis.core import QgsSpatialIndex, QgsFeatureRequest
import csv

grid_layer = QgsProject.instance().mapLayersByName("grid_montevideo")[0] #obtenemos la grilla roja
features = grid_layer.getFeatures()# obtenemos los cuadraditos rojos
data = QgsProject.instance().mapLayersByName('Marco2011_SEG_Montevideo_Total')[0]# obtenemos la capa de segmentos sensales
index = QgsSpatialIndex(data.getFeatures())# obtenemos los indices de los segmentos
results = []
for feature in features:
    geom = feature.geometry()
    extent = geom.boundingBox()
    margin = 0
    extent_with_margin = QgsRectangle(
        extent.xMinimum() - margin,
        extent.yMinimum() - margin,
        extent.xMaximum() + margin,
        extent.yMaximum() + margin
    )
    intersecting_ids = index.intersects(extent_with_margin)
    request = QgsFeatureRequest().setFilterFids(intersecting_ids)
    pob_estimada = 0
    for other_feature in data.getFeatures(request):
        if other_feature.geometry().intersects(geom):
            atributos = other_feature.attributes()
            ptot=atributos[28]
            area_original=atributos[0]
            intersection_geom = other_feature.geometry().intersection(geom)
            area_intersection = intersection_geom.area()
            pob_estimada += (ptot/area_original * area_intersection)
    results.append({'id': feature.id(), 'pob_estimada': pob_estimada})
csv_file = '/opt/projects/marvik/ml/ml/population.csv'  # Cambia esta ruta por la que desees

# Escribir los resultados en el archivo CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'pob_estimada']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Resultados guardados en {csv_file}")