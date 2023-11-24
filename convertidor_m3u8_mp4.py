from moviepy.editor import VideoFileClip
import time


################################################################


# Reemplaza 'URL_DEL_ARCHIVO_M3U8' con tu enlace m3u8
url_m3u8 = 'https://www.udemy.com/assets/37161798/files/2021-10-29_10-57-39-0a97b9d019d2972d65c683319d4a6d77/2/hls/AVC_1920x1080_1600k_AAC-HE_64k/aa001dec7e9376ba6770e43f8f9617dbf888.m3u8?provider=cloudfront&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXRoIjoiMjAyMS0xMC0yOV8xMC01Ny0zOS0wYTk3YjlkMDE5ZDI5NzJkNjVjNjgzMzE5ZDRhNmQ3Ny8yLyIsImV4cCI6MTcwMDg3MTg2Nn0.ZpJxynpr8_B0xg1YM50kg1XFTCOy8fTBD3ovwEdI3U4&v=1'
output_file = 'h12.mp4'

# Medir el tiempo de inicio
start_time = time.time()

# Descargar y convertir el video
video = VideoFileClip(url_m3u8)
video.write_videofile(output_file, codec='libx264', audio_codec='aac',  threads=12)

# Medir el tiempo de fin
end_time = time.time()

# Calcular la duración
duration = end_time - start_time

print(output_file)
print(f"Tiempo de descarga: {duration} segundos\n\n\n")


################################################################


# Reemplaza 'URL_DEL_ARCHIVO_M3U8' con tu enlace m3u8
url_m3u8 = 'https://www.udemy.com/assets/37161798/files/2021-10-29_10-57-39-0a97b9d019d2972d65c683319d4a6d77/2/hls/AVC_1920x1080_1600k_AAC-HE_64k/aa001dec7e9376ba6770e43f8f9617dbf888.m3u8?provider=cloudfront&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXRoIjoiMjAyMS0xMC0yOV8xMC01Ny0zOS0wYTk3YjlkMDE5ZDI5NzJkNjVjNjgzMzE5ZDRhNmQ3Ny8yLyIsImV4cCI6MTcwMDg3MTg2Nn0.ZpJxynpr8_B0xg1YM50kg1XFTCOy8fTBD3ovwEdI3U4&v=1'
output_file = 'h56.mp4'

# Medir el tiempo de inicio
start_time = time.time()

# Descargar y convertir el video
video = VideoFileClip(url_m3u8)
video.write_videofile(output_file, codec='libx264', audio_codec='aac',  threads=56)

# Medir el tiempo de fin
end_time = time.time()

# Calcular la duración
duration = end_time - start_time

print(output_file)
print(f"Tiempo de descarga: {duration} segundos\n\n\n")


################################################################


# Reemplaza 'URL_DEL_ARCHIVO_M3U8' con tu enlace m3u8
url_m3u8 = 'https://www.udemy.com/assets/37161798/files/2021-10-29_10-57-39-0a97b9d019d2972d65c683319d4a6d77/2/hls/AVC_1920x1080_1600k_AAC-HE_64k/aa001dec7e9376ba6770e43f8f9617dbf888.m3u8?provider=cloudfront&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXRoIjoiMjAyMS0xMC0yOV8xMC01Ny0zOS0wYTk3YjlkMDE5ZDI5NzJkNjVjNjgzMzE5ZDRhNmQ3Ny8yLyIsImV4cCI6MTcwMDg3MTg2Nn0.ZpJxynpr8_B0xg1YM50kg1XFTCOy8fTBD3ovwEdI3U4&v=1'
output_file = 'h255.mp4'

# Medir el tiempo de inicio
start_time = time.time()

# Descargar y convertir el video
video = VideoFileClip(url_m3u8)
video.write_videofile(output_file, codec='libx264', audio_codec='aac',  threads=255)

# Medir el tiempo de fin
end_time = time.time()

# Calcular la duración
duration = end_time - start_time

print(output_file)
print(f"Tiempo de descarga: {duration} segundos\n\n\n")
