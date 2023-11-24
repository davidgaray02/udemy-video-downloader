from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from moviepy.editor import VideoFileClip

import time, os, re


# Ruta al directorio de datos del usuario de Chrome
user_data_dir = 'C:\\Users\\Usuario\\AppData\\Local\\Google\\Chrome\\User Data'

# Configuración de opciones de Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.binary_location = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'


# Inicia el navegador
driver = webdriver.Chrome(options=chrome_options)


##############################################################################################################


def esperar_pagina_cargada():
    try:
        # Espera a que la página termine de cargarse
        wait = WebDriverWait(driver, 25)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except:
        pass
    

def esperar_video_cargado():
    try:
        # Espera a que la página termine de cargarse
        wait = WebDriverWait(driver, 25)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
    except:
        pass
    

def obtener_link_video():
    esperar_video_cargado()
    log_recursos = driver.execute_script("return window.performance.getEntriesByType('resource');")
    videos_url = []
    # Ordenado de mayor a menor para luego filtrar el de mayor calidad
    calidades = ['3840x2160', '1920x1080', '1200x720', '1024x576', '768x432', '640x360']
    
    for video in log_recursos:
        if (video['name'].startswith("https://www.udemy.com/assets") or video['name'].startswith("https://mp4-c.udemycdn.com/") and "sprites" not in video['name']):
            videos_url.append(video['name'])

    if videos_url == []:
        videos_url.append("Video no encontrado")
        
    # Filtrar video de mayor calidad
    video_calidad_url = videos_url[0]
    video_calidad_encontrado = False

    for calidad in calidades:
        for video_url in videos_url:
            if calidad in video_url:
                video_calidad_url = video_url
                video_calidad_encontrado = True
                break
        if video_calidad_encontrado == True:
            break

    print('\nVideo link:', video_calidad_url)
    print('---------------------\n')
    return video_calidad_url


def crear_directorio_descargas():
    sufijo = 1
    nombre_directorio = re.sub(r'[<>:"/\|?*]', '-', driver.title)
    ruta_directorio = os.path.join(os.getcwd(), nombre_directorio)
    
    try:
        os.makedirs(ruta_directorio)
        nueva_ruta = ruta_directorio
    except:
        while True:
            nueva_ruta = f"{ruta_directorio} ({sufijo})"
            try:
                os.makedirs(nueva_ruta)
                break
            except:
                sufijo += 1
    
    ruta_directorio_videos = os.path.join(nueva_ruta, "Videos")
    ruta_directorio_recursos = os.path.join(nueva_ruta, "Recursos")
    ruta_directorio_preguntas = os.path.join(nueva_ruta, "Preguntas y Respuestas")
    
    os.makedirs(ruta_directorio_videos)
    os.makedirs(ruta_directorio_recursos)
    os.makedirs(ruta_directorio_preguntas)


    print(f"Directorio de descargas creado en '{nueva_ruta}'")
    
    ruta_archivo = os.path.join(nueva_ruta, "links_videos.txt")
    print(f"Links.txt creado en: {ruta_archivo}")

    with open(ruta_archivo, "w") as archivo:
        pass
    
    return nueva_ruta


def adelantar_video():
    try:
        video = driver.find_element(By.CLASS_NAME, "video-player--video-player--2DBqU")

        
        #driver.execute_script("arguments[0].requestFullscreen()", video)
        print("Video maximizado")

        
        time.sleep(5)
        esperar_video_cargado()
        driver.execute_script("arguments[0].currentTime = arguments[0].duration * 0.9", video)
        print("Video adelantado un 80%")

        # Si el video está pausado, reproducirlo
        is_paused = driver.execute_script("return arguments[0].paused", video)
        if is_paused:
            driver.execute_script("arguments[0].play()", video)
            print("Video en play")
            
        time.sleep(5)
        driver.execute_script("document.exitFullscreen()")
        #print("Video minimizado")
        
        print("Se adelanto correctamente el video")
        
    except Exception as e:
        print(f"No se pudo adelantar el video. Erro: {e}")

        

def cerrar_popup():
    try:
        time.sleep(2)
        boton_cerrar = driver.find_element(by=By.XPATH, value="//button[contains(@class, 'ud-btn ud-btn-medium ud-btn-ghost ud-heading-sm ud-btn-icon ud-btn-icon-medium ud-modal-close modal-module--close-button--b86KD')]")
        boton_cerrar.click()
        print("Popup cerrado correctamente")
    except:
        print("No se encontró ningún popup")
        
    
def descargar_m3u8_mp4(url_m3u8, output_file):
    try:
        video = VideoFileClip(url_m3u8)
        video.write_videofile(output_file)
    except Exception as e:
        print(f"No se pudo convertir el video. Error: {e}")

def limpiar_recursos():
    try:
        driver.execute_script('window.performance.clearResourceTimings();')
        print("Recursos limpiados")
    except Exception as e:
        print(f"No se pudo limpiar los recursos. Error: {e}")




##############################################################################################



driver.get("https://www.udemy.com")
esperar_pagina_cargada()
driver.get("https://www.udemy.com/course/django-angular/learn/lecture/29164442#content")
cerrar_popup()

ruta_directorio_descargas = crear_directorio_descargas()
ruta_archivo_links = os.path.join(ruta_directorio_descargas, "links_videos.txt")
print(f"\nRuta archivo: {ruta_archivo_links}")

# Iterar en cada video
time.sleep(2)
secciones = driver.find_elements(by=By.XPATH, value="//span[contains(@class, 'ud-accordion-panel-title')]")


for seccion in secciones:
    print(f"\n{seccion.text.upper()}")
    
    if seccion != secciones[0]:
        seccion.click()

    time.sleep(2)
    
    lecciones = driver.find_elements(by=By.XPATH, value="//span[contains(@class, 'curriculum-item-link--curriculum-item-title-content--1SLoR')]")
    
    for leccion in lecciones:
        leccion.click()
        
        nombre_leccion = leccion.text
        print(f"\nLeccion: {nombre_leccion}")            
        
        time.sleep(1)
        
        adelantar_video()
        
        time.sleep(2)
        
        video_link = obtener_link_video()

        with open(ruta_archivo_links, "a") as archivo_links:
            archivo_links.write(f"{nombre_leccion}\n")
            archivo_links.write(f"{video_link}\n")
            
            titulo_video = re.sub(r'[<>:"/\|?*]', '-', nombre_leccion)
            ruta_carpeta_videos =  os.path.join(ruta_directorio_descargas, "Videos")
            ruta_video = os.path.join(ruta_carpeta_videos, f"{titulo_video}.mp4")
            
            try:
                video = VideoFileClip(video_link).volumex(1.1)
                video.write_videofile(ruta_video,  codec='libx264', audio_codec='aac',  threads=12)
                
            except Exception as e:
                print(f"No se puedo descargar el video. Error: {e}")
                
        
        limpiar_recursos()
                
    seccion.click()


###########################---DESCARGAR VIDEOS---#####################################

num_linea = 1




        
# Cierra el navegador cuando hayas terminado
driver.quit()
