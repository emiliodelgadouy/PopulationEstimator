import math

from flask import Flask, request, jsonify, render_template_string
import pickle
import numpy as np
from keras.api.applications.vgg16 import VGG16, preprocess_input
from keras.src.utils import load_img, img_to_array
import keras
from flask import render_template


# Crear la aplicación Flask
app = Flask(__name__)

# Cargar el modelo y otros componentes necesarios
feature_extractor = VGG16(weights='imagenet', include_top=False, pooling='avg')
model = keras.models.load_model('./modelo.keras')
with open('./scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


def preprocess_new_image(image_path):
    """
    Preprocesa una imagen para ser utilizada con el modelo.
    """
    target_dimensions = (224, 224)
    try:
        # Cargar y redimensionar la imagen
        img = load_img(image_path, target_size=target_dimensions)
        img_data = img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)

        # Preprocesar la imagen
        img_data = preprocess_input(img_data)

        # Extraer características
        feature = feature_extractor.predict(img_data)
        return feature.flatten()
    except Exception as e:
        print(f"Error al procesar la imagen {image_path}: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para realizar predicción a partir de una imagen.
    """
    try:
        # Obtener archivo de imagen del cliente
        if 'image' not in request.files:
            return jsonify({"error": "No se envió ninguna imagen"}), 400

        image = request.files['image']
        image_path = f"./temp_{image.filename}"  # Ruta temporal para la imagen

        # Guardar la imagen temporalmente
        image.save(image_path)

        # Preprocesar la imagen
        features = preprocess_new_image(image_path)
        if features is None:
            return jsonify({"error": "Error al procesar la imagen"}), 500

        # Escalar características
        features = scaler.transform([features])

        # Realizar predicción
        prediction = model.predict(features)

        # Limpiar la imagen temporal
        import os
        os.remove(image_path)

        # Retornar la predicción
        return jsonify({"poblacion": float(math.floor(prediction[0][0]))}), 200

    except Exception as e:
        return jsonify({"error": f"Error al realizar la predicción: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
