import cv2
import numpy as np

# Coordenadas originales de la imagen proyectada (imagen de la cuadrícula)
points_projected = np.array([
    [79, 79],               # Esquina superior izquierda
    [1920 - 79, 79],        # Esquina superior derecha
    [79, 1080 - 79],        # Esquina inferior izquierda
    [1920 - 79, 1080 - 79]  # Esquina inferior derecha
])

# Coordenadas detectadas por la cámara (en la imagen capturada)
points_camera = np.array([
    [67, 80],    # Esquina superior izquierda detectada por la cámara
    [1867, 77],   # Esquina superior derecha detectada por la cámara
    [67, 1019],    # Esquina inferior izquierda detectada por la cámara
    [1845, 1023]    # Esquina inferior derecha detectada por la cámara
])

# Calcular la matriz de homografía
homography_matrix, status = cv2.findHomography(points_camera, points_projected)

# Imprimir la matriz de homografía
print("Matriz de homografía calculada:")
print(homography_matrix)
