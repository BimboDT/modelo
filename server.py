from flask import Flask, request, jsonify
from flask_cors import CORS

# Librerías
from ultralytics import YOLO    #type: ignore
import cv2
import requests   #type: ignore
import numpy as np
import oci  #type: ignore
from oci.config import from_file    #type: ignore
from oci.object_storage import ObjectStorageClient    #type: ignore
from io import BytesIO

# Configura el cliente de Object Storage
config = oci.config.from_file()  # Carga la configuración desde el archivo .oci/config
object_storage_client = ObjectStorageClient(config)

# Parámetros de tu bucket
namespace = object_storage_client.get_namespace().data  # Obtén el namespace en el que trabajar
bucket_name = 'fotos-web'
region = config['region']
index = 0

## Server configuration
server = Flask(__name__)
CORS(server)

# Cargar el modelo YOLO
model = YOLO('bestV3.pt')

# Función para descargar la imagen desde una URL y convertirla al formato OpenCV
def url_to_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_array = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return image
    else:
        return None

# Función para subir la imagen procesada a Oracle Cloud Storage
def upload_image(namespace, bucket_name, object_name, image):
    object_storage_client.put_object(
        namespace,
        bucket_name,
        object_name,
        image
    )
    url = f"https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{object_name}"
    return url


# Ruta de prueba
@server.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API funcionando correctamente"}), 200

# Ruta para predicción
@server.route('/predict', methods=['POST'])
def predictJSON():
    global index

    min_confidence = 0.6


    # Cargar la imagen
    data = request.json
    imgUrl = data['imageUrl']

    # Descargar la imagen
    image = url_to_image(imgUrl)
    if image is None:
        return jsonify({"message": "No se pudo obtener la imagen desde la URL"}), 400

    # Realizar la inferencia con YOLO
    results = model(image)

    # Índices de las clases
    caja_class_index = 0
    oclusion_class_index = 1

    detecciones_caja = 0
    oclusion_detectada = False

    # Extraer información de detecciones
    for box in results[0].boxes:
        confidence = float(box.conf)  # Confianza de la predicción
        class_id = int(box.cls)  # Clase

        # Filtrar detecciones con confianza > min_confidence
        if confidence > min_confidence:
            if class_id == caja_class_index:
                detecciones_caja += 1  # Contar detecciones de cajas
            elif class_id == oclusion_class_index:
                oclusion_detectada = True  # Detectar oclusiones

            # Dibujar las cajas y etiquetas en la imagen
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
            label = f"Clase {class_id} ({confidence:.2f})"  # Etiqueta de cada detección
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 0), 2)

    foto_binaria = cv2.imencode('.jpg', image)[1].tobytes()
    file_data = BytesIO(foto_binaria)

    # Subir la imagen procesada a Oracle Cloud Storage
    url = upload_image(namespace, bucket_name, f"Procesado/image_{index}.jpg", file_data)
    print(f"Imagen procesada subida a: {url}")
    index = index + 1

    # Devolver los resultados en formato JSON y la URL
    # Número de cajas y Booleano de oclusiones
    return jsonify({
        'detecciones_caja': detecciones_caja,
        'oclusion_detectada': oclusion_detectada,
        'url': url})


if __name__ == '__main__':
    # Iniciar el servidor
    server.run(debug=False, host='0.0.0.0', port=8081)
