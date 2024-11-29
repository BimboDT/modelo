import os
import shutil

def create_directories(output_dir):
    train_dir = os.path.join(output_dir, "train")
    val_dir = os.path.join(output_dir, "validation")
    test_dir = os.path.join(output_dir, "test")
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    return train_dir, val_dir, test_dir

def split_dataset(input_dir, output_dir):
    images = sorted([f for f in os.listdir(input_dir) if f.endswith(".jpg") or f.endswith(".png")])
    train_dir, val_dir, test_dir = create_directories(output_dir)
    
    for i, image_file in enumerate(images):
        # Obtener el archivo JSON correspondiente
        json_file = os.path.splitext(image_file)[0] + ".json"
        
        # Revisar que ambos archivos existan
        image_path = os.path.join(input_dir, image_file)
        json_path = os.path.join(input_dir, json_file)
        if not os.path.exists(json_path):
            print(f"Warning: No JSON file found for {image_file}. Skipping...")
            continue
        
        # Asignar la imagen y JSON al conjunto correspondiente
        if i % 7 < 5:  # Aproximadamente 70% para train
            target_dir = train_dir
        elif i % 7 == 5:  # Aproximadamente 15% para validation
            target_dir = val_dir
        else:  # Aproximadamente 15% para test
            target_dir = test_dir

        # Copiar archivos a la carpeta correspondiente
        shutil.copy2(image_path, target_dir)
        shutil.copy2(json_path, target_dir)

# Directorio de entrada y salida
input_dir = "Fotos_Modelo_Juntas2"
output_dir = "Modelo_para_entrenar2"

# Ejecutar la división de datos
split_dataset(input_dir, output_dir)
