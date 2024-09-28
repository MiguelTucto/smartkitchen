import os
import shutil
from sklearn.model_selection import train_test_split

# Directorios
augmented_images_dir = "D:/Projects/20241089/smartkitchenv1/model/response/images"  # Carpeta con las 20020 imágenes aumentadas
augmented_labels_dir = "D:/Projects/20241089/smartkitchenv1/model/response/label"  # Carpeta con las etiquetas correspondientes

train_images_dir = "D:/Projects/20241089/smartkitchenv1/model/newdatav3/images/train/"  # Carpeta final para imágenes de entrenamiento
train_labels_dir = "D:/Projects/20241089/smartkitchenv1/model/newdatav3/label/train/"  # Carpeta final para etiquetas de entrenamiento
val_images_dir = "D:/Projects/20241089/smartkitchenv1/model/newdatav3/images/validation/"      # Carpeta final para imágenes de validación
val_labels_dir = "D:/Projects/20241089/smartkitchenv1/model/newdatav3/label/validation/"      # Carpeta final para etiquetas de validación

# Crear las carpetas de salida si no existen
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Listar todas las imágenes aumentadas
augmented_images = [f for f in os.listdir(augmented_images_dir) if f.endswith('.jpg')]

# Asegurarse de que las etiquetas correspondientes existen para cada imagen
augmented_labels = [f.replace('.jpg', '.txt') for f in augmented_images if os.path.exists(os.path.join(augmented_labels_dir, f.replace('.jpg', '.txt')))]

# Dividir el conjunto de datos en 80% train y 20% val
train_images, val_images = train_test_split(augmented_images, test_size=0.2, random_state=42)

# Mover imágenes y etiquetas a las carpetas correspondientes

# Para el conjunto de entrenamiento
for image_name in train_images:
    # Ruta completa de la imagen y la etiqueta
    image_path = os.path.join(augmented_images_dir, image_name)
    label_path = os.path.join(augmented_labels_dir, image_name.replace('.jpg', '.txt'))

    # Mover imagen
    shutil.move(image_path, os.path.join(train_images_dir, image_name))

    # Mover etiqueta correspondiente
    shutil.move(label_path, os.path.join(train_labels_dir, image_name.replace('.jpg', '.txt')))

# Para el conjunto de validación
for image_name in val_images:
    # Ruta completa de la imagen y la etiqueta
    image_path = os.path.join(augmented_images_dir, image_name)
    label_path = os.path.join(augmented_labels_dir, image_name.replace('.jpg', '.txt'))

    # Mover imagen
    shutil.move(image_path, os.path.join(val_images_dir, image_name))

    # Mover etiqueta correspondiente
    shutil.move(label_path, os.path.join(val_labels_dir, image_name.replace('.jpg', '.txt')))

print(f"Separación completada: {len(train_images)} imágenes en train, {len(val_images)} imágenes en val.")
