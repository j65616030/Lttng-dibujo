import cv2
import numpy as np
import csv


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

        # Verificar si se encontraron contornos
        for contour in contours:
            # Verificar si el contorno es válido
            if contour is not None and len(contour) >= 3:
                try:
                    area = cv2.contourArea(contour)
                    if area > 100:  # ajustar el valor según sea necesario
                        # Calcular el color promedio dentro del contorno
                        x, y, w, h = cv2.boundingRect(contour)
                        roi = frame2[y:y+h, x:x+w]
                        color_promedio = np.mean(roi, axis=(0, 1)).astype(int)

                        # Dibujar los contornos en el fotograma original
                        cv2.drawContours(frame2, [contour], -1, (int(color_promedio[0]), int(color_promedio[1]), int(color_promedio[2])), 3)

                        # Almacenar datos de movimiento
                        datos_movimiento.append({
                            'num_fotograma': num_fotograma,
                            'x': x,
                            'y': y,
                            'w': w,
                            'h': h,
                            'area': area,
                            'color': (color_promedio[0], color_promedio[1], color_promedio[2])
                        })
                    else:
                        # Área pequeña, almacenar como si fuera 0
                        datos_movimiento.append({
                            'num_fotograma': num_fotograma,
                            'x': 0,
                            'y': 0,
                            'w': 0,
                            'h': 0,
                            'area': 0,
                            'color': (0, 0, 0)
                        })
                except cv2.error as e:
                    print(f"Error al calcular el área del contorno: {e}")
            else:
                # No hay contorno, rellenar con valores 0
                datos_movimiento.append({
                    'num_fotograma': num_fotograma,
                    'x': 0,
                    'y': 0,
                    'w': 0,
                    'h': 0,
                    'area': 0,
                    'color': (0, 0, 0)
                })

        # Mostrar el fotograma con los contornos
        cv2.imshow('Frame', frame2)

        # Esperar a que se presione una tecla
        if cv2.waitKey(1) == ord('q'):
            break

        # Actualizar el fotograma anterior
        gray1 = gray2

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

    return datos_movimiento, ancho_original, alto_original


# Ejecutar la función
# ...

# Ejecutar la función
datos_movimiento, ancho_original, alto_original = analizar_video_con_contornos('ruta_al_video.mp4')

# Guardar datos de movimiento en un archivo de texto
if datos_movimiento is not None:
    with open('datos_movimiento.txt', 'w') as f:
        f.write(f"Tamaño original del video: {ancho_original}x{alto_original}\n\n")
        f.write("Datos de movimiento:\n")
        for dato in datos_movimiento:
            f.write(f"Fotograma {dato['num_fotograma']}: x={dato['x']}, y={dato['y']}, w={dato['w']}, h={dato['h']}, área={dato['area']}, color={dato['color']}\n")
else:
    print("No se pudo analizar el video.")