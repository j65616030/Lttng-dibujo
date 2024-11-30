import cv2
import numpy as np
import time

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

# Definir el rango de rojos
rojo_min = (150, 0, 0)
rojo_max = (255, 100, 100)

# Definir el color rosa claro
rosa_claro = (255, 105, 180)

# Variable para almacenar el color del contorno que se mantuvo durante varios fotogramas
color_mantenido = None

# Variables para almacenar el tiempo y la lista de puntos
# Variables para almacenar el tiempo y la lista de puntos
tiempo_ultimo_punto = 0
trayectoria = []

# Dibujar los contornos por frame
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.moveWindow("Video", 100, 100)  # Mover la ventana a la posición (100, 100)
for frame, contornos_frame in contornos_por_frame.items():
    # Crear una imagen en blanco para el frame actual
    imagen = np.zeros((max_y, max_x, 3), np.uint8)

    # Dibujar los contornos en la imagen
    for contorno in contornos_frame:
        # Comprobar si el color del contorno está dentro del rango de rojos
        if rojo_min[0] <= contorno["color"][0] <= rojo_max[0] and rojo_min[1] <= contorno["color"][1] <= rojo_max[1] and rojo_min[2] <= contorno["color"][2] <= rojo_max[2]:
            # Dibujar un punto en el centro del contorno
            punto_x = contorno["x"] + contorno["w"] // 2
            punto_y = contorno["y"] + contorno["h"] // 2
            cv2.circle(imagen, (punto_x, punto_y), 5, rosa_claro, -1)

            # Comprobar si el punto está dentro de la área de 500x500
            if trayectoria and abs(punto_x - trayectoria[-1][0]) < 500 and abs(punto_y - trayectoria[-1][1]) < 500:
                # Agregar el punto a la lista de puntos de la trayectoria
                trayectoria.append((punto_x, punto_y))
            else:
                # Reiniciar la lista de puntos de la trayectoria
                trayectoria = [(punto_x, punto_y)]

            # Dibujar la trayectoria
            if time.time() - tiempo_ultimo_punto < 10:
                for i in range(1, len(trayectoria)):
                    cv2.line(imagen, trayectoria[i-1], trayectoria[i], (0, 0, 255), 2)
            else:
                # Reiniciar la lista de puntos de la trayectoria
                trayectoria = []
        else:
            # Dibujar un punto en el centro del contorno
            punto_x = contorno["x"] + contorno["w"] // 2
            punto_y = contorno["y"] + contorno["h"] // 2
            cv2.circle(imagen, (punto_x, punto_y), 5, (0, 255, 0), -1)

    # Mostrar la imagen
    cv2.imshow("Video", imagen)
    cv2.waitKey(1)  # Retardo de 1 milisegundo

# Cerrar la ventana
cv2.destroyAllWindows()