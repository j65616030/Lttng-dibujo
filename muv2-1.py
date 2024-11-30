import cv2
import numpy as np


def analizar_video_con_contornos(video_path, num_frames_acumular=650, umbral_acumulador=2, kernel_size=5):
    """
    Analiza un video, detectando movimiento y dibujando contornos.


    Args:
        video_path (str): Ruta al video.
        num_frames_acumular (int): Número de frames a acumular para suavizar el movimiento.
        umbral_acumulador (int): Umbral para la detección de movimiento en la acumulación.
        kernel_size (int): Tamaño del kernel para la operación morfológica.
    """

    cap = cv2.VideoCapture(video_path)

    # Leer el primer fotograma
    ret, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Inicializar acumulador con el mismo tamaño y tipo de dato que gray1
    acumulador = np.zeros_like(gray1, dtype=np.float32)

    # Inicializar archivo para guardar la información de los contornos
    with open("contornos.txt", "w") as archivo:
        archivo.write("Frame,X,Y,W,H,Color_R,Color_G,Color_B\n")

    frame_actual = 0
    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break

        # Convertir a escala de grises
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Calcular la diferencia (asegurando tipo de dato float32)
        diff = cv2.absdiff(gray1, gray2).astype(np.float32)

        # Acumular diferencias
        cv2.accumulateWeighted(diff, acumulador, 0.2)

        # Aplicar umbral y convertir a uint8 para cv2.findContours
        _, thresh = cv2.threshold(acumulador, umbral_acumulador, 255, cv2.THRESH_BINARY)
        thresh = thresh.astype(np.uint8)

        # Encontrar contornos
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar contornos
        for contour in contours:
            # Calcular el área del contorno
            area = cv2.contourArea(contour)

            # Calcular el color promedio dentro del contorno
            x, y, w, h = cv2.boundingRect(contour)
            roi = frame2[y:y+h, x:x+w]
            color_promedio = np.mean(roi, axis=(0, 1)).astype(int)

            # Dibujar el contorno con el color promedio
            cv2.drawContours(frame2, [contour], -1, (int(color_promedio[0]), int(color_promedio[1]), int(color_promedio[2])), 3)

            # Guardar la información del contorno en el archivo
            with open("contornos.txt", "a") as archivo:
                archivo.write(f"{frame_actual},{x},{y},{w},{h},{color_promedio[0]},{color_promedio[1]},{color_promedio[2]}\n")

        # Mostrar el resultado
        cv2.imshow('Frame', frame2)

        if cv2.waitKey(1) == ord('q'):
            break

        gray1 = gray2
        frame_actual += 1

    cap.release()
    cv2.destroyAllWindows()


# Ejemplo de uso:
video_path = 'mi_video1.mp4'
analizar_video_con_contornos(video_path)