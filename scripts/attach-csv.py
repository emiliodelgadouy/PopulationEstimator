import csv
from qgis.core import QgsProject, QgsField, edit
from PyQt5.QtCore import QVariant

layer = QgsProject.instance().mapLayersByName('grid_montevideo')[0]

csv_file = '/opt/projects/marvik/ml/ml/resultados_clustering.csv'  # Reemplaza con la ruta a tu archivo CSV

# Leer datos del CSV y crear un diccionario data_dict
data_dict = {}
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    csv_fields = reader.fieldnames
    for row in reader:
        data_dict[int(row['id'])] = row  # Suponiendo que el campo 'id' es entero

# Agregar los campos del CSV a la capa si no existen
csv_fields.remove('id')  # Remover 'id' ya que ya está en la capa
fields_to_add = []
existing_fields = [field.name() for field in layer.fields()]
for field_name in csv_fields:
    if field_name not in existing_fields:
        fields_to_add.append(QgsField(field_name, QVariant.String))  # Cambia el tipo si es necesario

if fields_to_add:
    layer.dataProvider().addAttributes(fields_to_add)
    layer.updateFields()

# Asignar datos del CSV a las features
with edit(layer):
    for feature in layer.getFeatures():
        feature_id = feature['id']
        if feature_id in data_dict:
            csv_row = data_dict[feature_id]
            for field_name in csv_fields:
                feature[field_name] = csv_row[field_name]
            layer.updateFeature(feature)
