import cv2
import numpy as np

# Cargar la imagen capturada por la cámara
image = cv2.imread('E:/homografiav2.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un desenfoque para reducir el ruido y mejorar la detección
gray_blurred = cv2.GaussianBlur(gray, (15, 15), 0)

# Usar la función HoughCircles para detectar círculos
circles = cv2.HoughCircles(
    gray_blurred,
    cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
    param1=50, param2=30, minRadius=20, maxRadius=100
)

# Asegurarse de que se detectaron círculos
if circles is not None:
    # Convertir las coordenadas de los círculos a enteros
    circles = np.round(circles[0, :]).astype("int")

    # Dibujar los círculos detectados y obtener sus radios
    for (x, y, r) in circles:
        cv2.circle(image, (x, y), r, (0, 255, 0), 4)  # Dibuja el círculo
        print(f"Centro: ({x}, {y}), Radio: {r}")

    # Mostrar la imagen con los círculos detectados
    cv2.imshow("Círculos detectados", image)
    cv2.waitKey(0)
