import requests
import os
from urllib.parse import unquote
from pathlib import Path

def descargar_archivos(urls, carpeta_destino):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    for url in urls:
        nombre_archivo = unquote(url).split('/')[-1]  # Limpiar la URL y obtener el nombre del archivo
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
        
        respuesta = requests.get(url)
        
        with open(ruta_archivo, 'wb') as archivo:
            archivo.write(respuesta.content)

    print("Descarga completada")

# Ejemplo de uso
urls_de_descarga = [
    "https://att-c.udemycdn.com/2023-08-14_11-17-49-6503372b8114d5a8e48270297578bfb2/original.exe?response-content-disposition=attachment%3B+filename%3Dnvm-setup%252B%25282%2529.exe&Expires=1701194949&Signature=WC5QAtxqLJ3FsIaLtSydwjsJ05rB4aW9Dw75eFd-OFV1-Wrs1rS7aS7pZ5p-2fNcv736~ozw2Z31STdz65UBk1QpSqs7z1hAUAYr1xAH2U53uYQeMGouvTrED7~W86AFCj~Uw28ISmBqUKV7rkmqTPhHJUUEsKhwea~19B7fUauYok2zQbwOJQc4m5y3kiSVBWjsaV593yzWSPIIpvkEzPUfAQ4su6zKYBJxuOFQjSwHrWiKULUpqF6wnJLW6s6Sfb~zjrUX7VJbG06nHmimkN21jDiCit1kYG5lW-3LY1d1wxhFoNaS2tjv7VlVcryWu4ViRbW80J1huoN5PoWnFw__&Key-Pair-Id=K3MG148K9RIRF4"
]
carpeta_destino = r"C:\Users\Usuario\Desktop\udemy-video-downloader"
descargar_archivos(urls_de_descarga, carpeta_destino)
