import cv2
import numpy as np

def analizar_video_con_contornos(video_path):
    # Inicializar la captura de video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error al abrir el video '{video_path}'")
        return None

    # Obtener el tamaño original del video
    ancho_original = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto_original = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Leer el primer fotograma
    ret, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Crear una imagen auxiliar para acumular los frames
    acumulador = np.zeros_like(frame1)

    # Inicializar lista para almacenar datos de movimiento
    datos_movimiento = []

    # Inicializar contador de fotogramas
    num_fotograma = 0

    while cap.isOpened():
        # Leer el siguiente fotograma
        ret, frame2 = cap.read()
        if not ret:
            break

        # Incrementar contador de fotogramas
        num_fotograma += 1

        # Convertir a escala de grises
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Calcular la diferencia entre los dos fotogramas
        diff = cv2.absdiff(gray1, gray2)

        # Aplicar umbral para destacar el movimiento
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        # Eliminar ruido mediante operaciones morfológicas
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Encontrar contornos en la imagen umbralizada
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Acumular los contornos en la imagen auxiliar
        acumulador = cv2.addWeighted(acumulador, 0.95, frame2, 0.05, 0)

        # Dibujar los contornos en la imagen auxiliar
        for contour in contours:
            cv2.drawContours(acumulador, [contour], -1, (0, 255, 0), 3)

        # Mostrar la imagen auxiliar
        cv2.imshow('Frame', acumulador)

        # Esperar a que se presione una tecla
        if cv2.waitKey(1) == ord('q'):
            break

        # Actualizar el fotograma anterior
        gray1 = gray2

        # Almacenar datos de movimiento
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            color_promedio = np.mean(acumulador[y:y+h, x:x+w], axis=(0, 1)).astype(int)
            datos_movimiento.append({
                'num_fotograma': num_fotograma,
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'area': area,
                'color': (color_promedio[0], color_promedio[1], color_promedio[2])
            })

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

    # Guardar datos de movimiento en un archivo de texto
    with open("datos_movimiento2.txt", "w") as archivo:
        archivo.write("Tamaño original del video: " + str(ancho_original) + "x" + str(alto_original) + "\n\n")
        archivo.write("Datos de movimiento:\n")
        for dato in datos_movimiento:
            archivo.write("Fotograma " + str(dato['num_fotograma']) + ": x=" + str(dato['x']) + ", y=" + str(dato['y']) + ", w=" + str(dato['w']) + ", h=" + str(dato['h']) + ", área=" + str(dato['area']) + ", color=" + str(dato['color']) + "\n")

    return datos_movimiento, ancho_original, alto_original


# Ejecutar la función
video_path = "tu_video1.mp4"
datos_movimiento, ancho_original, alto_original = analizar_video_con_contornos(video_path)