import cv2
import numpy as np

# Leer el archivo de contornos y determinar el tamaño correcto
max_x = 0
max_y = 0
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
            "color": (int(valores[6]), int(valores[5]), int(valores[7]))
        }
        contornos.append(contorno)
        if contorno["x"] + contorno["w"] > max_x:
            max_x = contorno["x"] + contorno["w"]
        if contorno["y"] + contorno["h"] > max_y:
            max_y = contorno["y"] + contorno["h"]

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
    imagen = np.zeros((max_y, max_x, 3), np.uint8)

    # Dibujar los contornos en la imagen
    for contorno in contornos_frame:
        cv2.rectangle(imagen, (contorno["x"], contorno["y"]), (contorno["x"] + contorno["w"], contorno["y"] + contorno["h"]), contorno["color"], 3)
        area = contorno["w"] * contorno["h"]
        cv2.putText(imagen, f"Área: {area}", (contorno["x"], contorno["y"] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, contorno["color"], 2)

    # Mostrar la imagen y esperar un tiempo
    cv2.imshow("Video", imagen)
    cv2.waitKey(15)  # Retardo de 100 milisegundos

# Cerrar la ventana
cv2.destroyAllWindows()