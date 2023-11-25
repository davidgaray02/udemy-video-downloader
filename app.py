from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from moviepy.editor import VideoFileClip

import time, os, re, json


# Ruta al directorio de datos del usuario de Chrome
user_data_dir = 'C:\\Users\\Usuario\\AppData\\Local\\Google\\Chrome\\User Data'

# Configuración de opciones de Chrome y descarga PDF
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

settings = {
    "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }


chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument('--enable-print-browser')
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.add_argument('--start-maximized')
# Inicia el navegador
driver = webdriver.Chrome(options=chrome_options)



##############################################################################################################


def formatear_url_curso(url):
    if "?" in url:
        url = url.split('?')[0]
    else:
        url = url.split('#')[0]    
    return url

def formatear_nombre_archivo(nombre_archivo):
    nombre_archivo = re.sub(r'[<>:"/\|?*]', '-', nombre_archivo)
    return nombre_archivo



def esperar_pagina_cargada():
    try:
        # Espera a que la página termine de cargarse
        wait = WebDriverWait(driver, 25)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except:
        pass



def descargar_pagina_pdf(nombre_pdf):
    try:    
        esperar_pagina_cargada()
        driver.execute_script('document.title = "' + nombre_pdf + '"; window.print();')
        time.sleep(3)
        print("Se descargó pregunta como PDF")
            
    except Exception as e:
        print(f"No se pudo descargar PDF. Error: {e}")
        
        

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
    nombre_curso = driver.find_element(by=By.XPATH, value="//a[contains(@class, 'ud-text-md header--header-text--3Z4po header--header-link--1gRxA truncate-with-tooltip--ellipsis--2-jEx')]")
    nombre_directorio = formatear_nombre_archivo(nombre_curso.text)
    print(nombre_directorio)
    
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
    
    global ruta_directorio_videos, ruta_directorio_recursos, ruta_directorio_preguntas, ruta_archivo_links
    ruta_directorio_videos = os.path.join(nueva_ruta, "Videos")
    ruta_directorio_recursos = os.path.join(nueva_ruta, "Recursos")
    ruta_directorio_preguntas = os.path.join(nueva_ruta, "Preguntas")
    ruta_archivo_links = os.path.join(nueva_ruta, "links_videos.txt")
    
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
        #print("Video maximizado")
        time.sleep(2)
        esperar_video_cargado()
        driver.execute_script("arguments[0].currentTime = arguments[0].duration * 0.9", video)
        print("Video adelantado un 80%")

        # Si el video está pausado, reproducirlo
        is_paused = driver.execute_script("return arguments[0].paused", video)
        if is_paused:
            driver.execute_script("arguments[0].play()", video)
            print("Video en play")
            
        time.sleep(6)
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
        print("No se encontró ningún popup para cerrar")
        
    
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
        
        
def descargar_preguntas_pdf():
    driver.get(url_preguntas)
    esperar_pagina_cargada()
    time.sleep(1)
    cerrar_popup()

    preguntas = driver.find_elements(by=By.XPATH, value="//a[contains(@class, 'ud-heading-md ud-link-neutral question-list-question--title-link--1TykF')]")
    while True:
        try:
            boton_ver_mas = driver.find_element(by=By.XPATH, value="//button[contains(@class, 'ud-btn ud-btn-large ud-btn-secondary ud-heading-md question-list--load-more-button--RCfUT')]")
            boton_ver_mas.click()
            time.sleep(1.5)
        except NoSuchElementException:
            break


    links_preguntas = []
    for pregunta in preguntas:
        link_pregunta = pregunta.get_attribute('href')
        links_preguntas.append(link_pregunta)

    for link in links_preguntas:
        driver.get(link)
        esperar_pagina_cargada()
        time.sleep(1)
        titulo_pregunta = driver.find_element(by=By.XPATH, value="//h3[contains(@class, 'ud-heading-md question-details--title--1w2zn')]")
        titulo_pregunta = formatear_nombre_archivo(titulo_pregunta.text)
        descargar_pagina_pdf(titulo_pregunta)


def descargar_recursos():
    try:
        boton_recursos = leccion.find_element(by=By.XPATH, value="//button[contains(@aria-label, 'Lista de recursos')]")
        boton_recursos.click()
        print("Dropdown recursos abierto")
        time.sleep(2)

        ruta_carpeta_recurso = os.path.join(ruta_directorio_recursos, nombre_leccion)
        os.makedirs(ruta_carpeta_recurso)
        
        recursos = boton_recursos.find_elements(by=By.XPATH, value="//button[contains(@class, 'ud-btn ud-btn-large ud-btn-ghost ud-text-sm resource--resource--315Oy ud-block-list-item ud-block-list-item-small ud-block-list-item-neutral')]")
        cantidad_recursos = len(recursos)
        
        boton_recursos.click()
        print(f"CANTIDAD RECURSOS: {cantidad_recursos}")
        
        for i in range(1, 2):
            boton_recursos.click()
            time.sleep(2)
            for recurso in recursos:
                titulo_recurso = recurso.text
                icono_recurso = recurso.find_element(By.TAG_NAME, 'use')
                tipo_icono = icono_recurso.get_attribute('xlink:href')
                recurso.click()
                time.sleep(4)
                if tipo_icono != "#icon-downloadable-resource":
                    esperar_pagina_cargada()
                    url_recurso = driver.current_url            
                    ruta_recurso = os.path.join(ruta_carpeta_recurso, "links.txt")
                    
                    with open(ruta_recurso, "a") as archivo:
                        archivo.write(f"{url_recurso}\n")

                driver.switch_to.window(pestana_pricipal)

                
                print(f"Recurso '{titulo_recurso}' obtenido")
                time.sleep(3)
    except:
        print(f"No encontró el botón 'Recursos' o los recursos dentro\nError:")
        
        
        


##############################################################################################





url_entrada = "https://www.udemy.com/course/python-3-az/learn/lecture/25206942#overview"
url_base_curso = formatear_url_curso(url_entrada)
url_contenido = url_base_curso + "#content"
url_preguntas = url_base_curso + "#questions"

# Obtener nombre del curos y crear directorio de descargas
driver.get(url_base_curso)
time.sleep(2)
esperar_pagina_cargada()
cerrar_popup()
ruta_directorio_descargas = crear_directorio_descargas()
driver.quit()

# Reconfigurar el directorio de preguntas a directorio creado
prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    'savefile.default_directory': ruta_directorio_preguntas
}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)

# Descargar preguntas como PDF
#descargar_preguntas_pdf()

# Iterar en cada video y descargar
driver.get(url_contenido)
time.sleep(2)
pestana_pricipal = driver.current_window_handle


secciones = driver.find_elements(by=By.XPATH, value="//button[contains(@class, 'ud-btn ud-btn-large ud-btn-link ud-heading-md js-panel-toggler accordion-panel-module--panel-toggler--1RjML')]")
secciones = secciones

for seccion in secciones:
    esta_expandido = seccion.get_attribute('aria-expanded')
    print(f"\n{seccion.text.upper()}")
    
    if esta_expandido == "false":
        seccion.click()

    time.sleep(2)
    
    
    lecciones = driver.find_elements(by=By.XPATH, value="//div[contains(@class, 'item-link item-link--common--RP3fp ud-custom-focus-visible')]")
    
    for leccion in lecciones:
        leccion.click()
        
        nombre_leccion = leccion.find_element(by=By.XPATH, value="//span[contains(@class, 'curriculum-item-link--curriculum-item-title-content--1SLoR')]")
        nombre_leccion = nombre_leccion.text
        print(f"\nLeccion: {nombre_leccion}")      
        descargar_recursos()      
        '''
        time.sleep(1)
        adelantar_video()
        
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
                
        '''
        limpiar_recursos()
                
    seccion.click()

# Cierra el navegador cuando hayas terminado
driver.quit()
    