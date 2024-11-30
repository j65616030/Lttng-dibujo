import cv2
import numpy as np

# Leer el archivo de contornos
contornos = []
with open("contornos.txt", "r") as archivo:
    next(archivo)  # Saltar la línea de cabecera
    for línea in archivo:
        valores = línea.strip().split(",")
        contorno = {
            "frame": int(valores[0]),
            "x": int(valores[1]),
            "y": int(valores[2]),
            "w": int(valores[3]),
            "h": int(valores[4]),
            "color": (int(valores[5]), int(valores[6]), int(valores[7]))
        }
        contornos.append(contorno)

# Agrupar los contornos por frames
contornos_por_frame = {}
for contorno in contornos:
    if contorno["frame"] not in contornos_por_frame:
        contornos_por_frame[contorno["frame"]] = []
    contornos_por_frame[contorno["frame"]].append(contorno)

# Dibujar los contornos por frame
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.moveWindow("Video", 100, 100)  # Mover la ventana a la posición (100, 100)
for frame, contornos_frame in contornos_por_frame.items():
    # Crear una imagen en blanco para el frame actual
    imagen = np.zeros((600, 800, 3), np.uint8)

    # Dibujar los contornos en la imagen
    for contorno in contornos_frame:
        cv2.rectangle(imagen, (contorno["x"], contorno["y"]), (contorno["x"] + contorno["w"], contorno["y"] + contorno["h"]), contorno["color"], 3)

    # Mostrar la imagen
    cv2.imshow("Video", imagen)
    cv2.waitKey(30)  # Retardo de 30 milisegundos

# Cerrar la ventana
cv2.destroyAllWindows()