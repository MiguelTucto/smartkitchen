import os
from collections import defaultdict

# Directorios de imágenes y etiquetas
ruta_labels = 'D:/Projects/20241089/smartkitchenv1/model/newdatav3/label/train'

# Diccionario para contar las apariciones de cada clase
conteo_clases = defaultdict(int)

mapeo_clases={
    '0': 'Apple',
    '1': 'Banana',
    '2': 'Carrot',
    '3': 'Cucumber',
    '4': 'Lemon',
    '5': 'Mango',
    '6': 'Orange',
    '7': 'Potato',
    '8': 'Tomato',
    '9': 'Zucchini'
}

# Recorrer todos los archivos de etiquetas (.txt)
for archivo_label in os.listdir(ruta_labels):
    if archivo_label.endswith('.txt'):
        ruta_archivo = os.path.join(ruta_labels, archivo_label)
        with open(ruta_archivo, 'r') as f:
            # Leer todas las líneas del archivo
            for linea in f:
                # Cada línea tiene el formato: class_id x_center y_center width height
                # Nos interesa el class_id (el primer valor)
                class_id = linea.split()[0]
                conteo_clases[class_id] += 1

# Mostrar el conteo por clase
for class_id, count in conteo_clases.items():
    nombre_clase = mapeo_clases.get(class_id, 'Clase desconocida')
    print(f"{nombre_clase}: {count} imágenes")

