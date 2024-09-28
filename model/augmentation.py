import albumentations as A
import cv2
import os
import shutil
from random import randint

# Definir las cantidades objetivo calculadas para cada clase
target_images_per_class = {
    'Apple': 1942,
    'Banana': 2000,
    'Carrot': 1667,
    'Cucumber': 1123,
    'Lemon': 1594,
    'Mango': 1404,
    'Orange': 1704,
    'Potato': 2005,
    'Tomato': 2262,
    'Zucchini': 1016
}

# Directorios de imágenes y etiquetas
images_dir = "D:/Projects/20241089/smartkitchenv1/model/newdata/images/train"
labels_dir = "D:/Projects/20241089/smartkitchenv1/model/newdata/labels/train"
output_images_dir = "D:/Projects/20241089/smartkitchenv1/model/response/images"
output_labels_dir = "D:/Projects/20241089/smartkitchenv1/model/response/label"

# Crear carpetas de salida si no existen
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_labels_dir, exist_ok=True)

# Transformaciones de augmentación
augmentations = A.Compose([
    A.RandomRotate90(p=0.5),               # Rotación aleatoria
    A.HorizontalFlip(p=0.5),                         # Volteo horizontal o vertical
    A.RandomBrightnessContrast(p=0.2),     # Ajustes de brillo/contraste
    A.HueSaturationValue(p=0.3),           # Variaciones de color
    A.GaussNoise(p=0.2),                   # Añadir ruido
])

# Contar cuántas imágenes hay actualmente por clase
current_images_per_class = {cls: 0 for cls in target_images_per_class.keys()}

# Recorremos los archivos de etiquetas para contar cuántas imágenes hay por clase
for label_file in os.listdir(labels_dir):
    label_path = os.path.join(labels_dir, label_file)
    with open(label_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            class_id = int(line.split()[0])  # Obtener class_id de cada línea
            class_name = list(target_images_per_class.keys())[class_id]  # Convertir class_id a nombre de clase
            current_images_per_class[class_name] += 1

# Aplicar augmentación para alcanzar las cantidades objetivo
for class_name, current_count in current_images_per_class.items():
    target_count = target_images_per_class[class_name]

    if current_count < target_count:
        # Generar más imágenes hasta alcanzar el objetivo
        images_needed = target_count - current_count

        # Filtrar las imágenes de la clase correspondiente usando las etiquetas
        class_images = []
        class_labels = []
        for label_file in os.listdir(labels_dir):
            label_path = os.path.join(labels_dir, label_file)
            with open(label_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    class_id = int(line.split()[0])  # Obtener el class_id desde el archivo de etiquetas
                    if class_id == list(target_images_per_class.keys()).index(class_name):  # Comparar con la clase actual
                        image_name = label_file.replace('.txt', '.jpg')  # Suponiendo que el nombre de la imagen coincide con el .txt
                        class_images.append(image_name)
                        class_labels.append(label_file)
                        break  # Salir del bucle si se encuentra la clase

        # Generar imágenes aumentadas hasta alcanzar el número objetivo
        for _ in range(images_needed):
            # Seleccionar una imagen aleatoria de la clase para hacer augmentación
            random_idx = randint(0, len(class_images) - 1)
            image_path = os.path.join(images_dir, class_images[random_idx])
            label_path = os.path.join(labels_dir, class_labels[random_idx])

            image = cv2.imread(image_path)

            # Aplicar augmentación
            augmented = augmentations(image=image)['image']

            # Guardar la nueva imagen aumentada
            aug_image_name = f"aug_{_}_{class_images[random_idx]}"
            aug_image_path = os.path.join(output_images_dir, aug_image_name)
            cv2.imwrite(aug_image_path, augmented)

            # Copiar la etiqueta correspondiente (ya que la augmentación no afecta las coordenadas)
            aug_label_name = f"aug_{_}_{class_labels[random_idx]}"
            aug_label_path = os.path.join(output_labels_dir, aug_label_name)
            shutil.copy(label_path, aug_label_path)

print("Data augmentation completado.")
