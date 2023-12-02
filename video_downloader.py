import os
import re
from moviepy.editor import VideoFileClip
import threading

def descargar_video(nombre_leccion, video_link, semaphore, event):
    try:
        titulo_video = re.sub(r'[<>:"/\|?*]', '-', nombre_leccion)
        ruta_carpeta_videos = r'C:\Users\Usuario\Desktop\udemy-video-downloader\Django, Postgres y Angular - Integracion Fullstack (2)\Videos'
        ruta_video = os.path.join(ruta_carpeta_videos, f"{titulo_video}.mp4")

        video = VideoFileClip(video_link).volumex(1.1)
        video.write_videofile(ruta_video, codec='libx264', audio_codec='aac', threads=4)
        print(f"Video '{nombre_leccion}' descargado con éxito.")

    except Exception as e:
        print(f"No se pudo descargar el video '{nombre_leccion}'. Error: {e}")

    finally:
        semaphore.release()  # Libera el semáforo después de descargar
        event.set()  # Marca el evento como completado

def descargar_y_eliminar_videos(archivo, num_hilos):
    try:
        with open(archivo, 'r') as file:
            lines = file.readlines()

        semaphore = threading.Semaphore(num_hilos)
        threads = []

        while lines:
            event = threading.Event()
            for i in range(min(num_hilos, len(lines)//2)):
                nombre_leccion = lines[i * 2].strip()
                video_link = lines[i * 2 + 1].strip()

                semaphore.acquire()  # Adquiere el semáforo antes de iniciar un hilo
                thread = threading.Thread(target=descargar_video, args=(nombre_leccion, video_link, semaphore, event))
                thread.start()
                threads.append((thread, event))

            # Espera a que todos los eventos hayan sido marcados como completados
            for _, event in threads:
                event.wait()

            # Elimina las líneas procesadas del archivo
            lines = lines[num_hilos * 2:]

        # Elimina el archivo original y crea uno nuevo con las líneas restantes
        os.remove(archivo)
        with open(archivo, 'w') as file:
            file.writelines(lines)

    except FileNotFoundError:
        print(f"El archivo {archivo} no se encontró.")

if __name__ == "__main__":
    archivo_links = r'C:\Users\Usuario\Desktop\udemy-video-downloader\Django, Postgres y Angular - Integracion Fullstack\links_videos.txt'
    cantidad_hilos = 2
    descargar_y_eliminar_videos(archivo_links, cantidad_hilos)
