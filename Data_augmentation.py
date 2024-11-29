import cv2
import os
import json
import random
import numpy as np

def flip_horizontal(image, annotations):
    flipped_image = cv2.flip(image, 1)
    img_width = image.shape[1]
    
    for shape in annotations['shapes']:
        if shape['shape_type'] == 'rectangle':
            shape['points'][0][0] = img_width - shape['points'][0][0]
            shape['points'][1][0] = img_width - shape['points'][1][0]
            shape['points'][0][0], shape['points'][1][0] = min(shape['points'][0][0], shape['points'][1][0]), max(shape['points'][0][0], shape['points'][1][0])
    
    return flipped_image, annotations

def flip_vertical(image, annotations):
    flipped_image = cv2.flip(image, 0)
    img_height = image.shape[0]
    
    for shape in annotations['shapes']:
        if shape['shape_type'] == 'rectangle':
            shape['points'][0][1] = img_height - shape['points'][0][1]
            shape['points'][1][1] = img_height - shape['points'][1][1]
            shape['points'][0][1], shape['points'][1][1] = min(shape['points'][0][1], shape['points'][1][1]), max(shape['points'][0][1], shape['points'][1][1])
    
    return flipped_image, annotations

def change_brightness(image):
    value = random.uniform(0.75, 1.25)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * value, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def add_gaussian_noise(image):
    mean = 0
    std = random.uniform(0.01, 0.02)
    gauss = np.random.normal(mean, std, image.shape).astype('uint8')
    noisy_image = cv2.add(image, gauss)
    return noisy_image

def update_json_metadata(annotations, new_image_path, image):
    annotations['imagePath'] = new_image_path
    annotations['imageHeight'] = image.shape[0]
    annotations['imageWidth'] = image.shape[1]
    return annotations

def process_image(image_path, json_path, output_dir):
    image = cv2.imread(image_path)
    with open(json_path, 'r') as f:
        annotations = json.load(f)

    # Aplicar las transformaciones en secuencia a la misma imagen
    transformed_image, transformed_annotations = flip_horizontal(image, annotations.copy())
    transformed_image, transformed_annotations = flip_vertical(transformed_image, transformed_annotations)
    transformed_image = change_brightness(transformed_image)
    transformed_image = add_gaussian_noise(transformed_image)

    # Actualizar metadata en JSON
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    new_image_path = f"{base_name}_augmented.jpg"
    transformed_annotations = update_json_metadata(transformed_annotations, new_image_path, transformed_image)
    
    # Guardar imagen transformada y archivo JSON actualizado
    aug_image_path = os.path.join(output_dir, new_image_path)
    aug_json_path = os.path.join(output_dir, f"{base_name}_augmented.json")
    
    cv2.imwrite(aug_image_path, transformed_image)
    with open(aug_json_path, 'w') as f:
        json.dump(transformed_annotations, f, indent=4)

def augment_data(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            json_path = os.path.join(input_dir, os.path.splitext(filename)[0] + ".json")
            
            if os.path.exists(json_path):
                process_image(image_path, json_path, output_dir)

# Directorios de entrada y salida
input_dir = "Fotos"
output_dir = "Fotos_augmentation"

# Ejecutar el data augmentation
augment_data(input_dir, output_dir)
