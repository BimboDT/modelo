import os
import json

# Asignar IDs para las clases en YOLO
class_id_map = {"triangulo": 0, "cuadrado": 1, "rombo": 2}  # Mapa de clases para 'caja' y 'oclusion'

def convert_to_yolo(json_data, output_path):
    image_width = json_data['imageWidth']
    image_height = json_data['imageHeight']
    yolo_lines = []

    for shape in json_data['shapes']:
        label = shape['label']
        if label not in class_id_map:
            print(f"Warning: Label '{label}' not found in class_id_map. Skipping...")
            continue

        class_id = class_id_map[label]
        
        # Obtener coordenadas del rectángulo
        x_min, y_min = shape['points'][0]
        x_max, y_max = shape['points'][1]

        # Convertir a formato YOLO (centrado y normalizado)
        x_center = ((x_min + x_max) / 2) / image_width
        y_center = ((y_min + y_max) / 2) / image_height
        width = (x_max - x_min) / image_width
        height = (y_max - y_min) / image_height

        # Crear línea en formato YOLO
        yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        yolo_lines.append(yolo_line)

    # Guardar en archivo .txt en formato YOLO
    with open(output_path, 'w') as yolo_file:
        yolo_file.write("\n".join(yolo_lines))

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            json_path = os.path.join(folder_path, filename)
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file)

            # Crear el nombre de archivo de salida .txt para YOLO
            yolo_filename = os.path.splitext(filename)[0] + ".txt"
            yolo_path = os.path.join(folder_path, yolo_filename)

            # Convertir y guardar
            convert_to_yolo(json_data, yolo_path)

def convert_all_folders(base_dir):
    for folder_name in ["train", "validation", "test"]:
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.exists(folder_path):
            process_folder(folder_path)

# Directorio base que contiene train, validation y test
base_dir = "Modelo_para_entrenar2"
convert_all_folders(base_dir)
