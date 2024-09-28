import cv2

# Cargar la imagen capturada por la cámara
image = cv2.imread("E:/capture.png")

# Lista para almacenar las coordenadas
points = []

# Función para capturar las coordenadas con clic
def capture_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Coordenada capturada: ({x}, {y})")
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Dibuja un punto en la coordenada

# Mostrar la imagen
cv2.imshow("Selecciona los puntos de referencia", image)
cv2.setMouseCallback("Selecciona los puntos de referencia", capture_points)

# Esperar a que captures 4 puntos
while len(points) < 4:
    cv2.imshow("Selecciona los puntos de referencia", image)
    cv2.waitKey(1)

# Imprimir los puntos capturados
print("Coordenadas capturadas:", points)
cv2.destroyAllWindows()
