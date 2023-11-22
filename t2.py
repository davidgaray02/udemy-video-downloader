from selenium import webdriver
import time

def obtener_recursos():
    time.sleep(3)
    # Obtiene el log de la red
    log_entries = driver.get_log('performance')

    # Imprime información sobre las solicitudes
    for entry in log_entries:
        try:
            request_data = entry['message']['params']['response']
            print('URL del recurso:', request_data['url'])
            print('Tipo de recurso:', request_data['mimeType'])
            print('--------------')
        except KeyError:
            pass

# Ruta al directorio de datos del usuario de Chrome
user_data_dir = r'C:\\Users\\Usuario\\AppData\\Local\\Google\\Chrome\\User Data'

# Configuración de opciones de Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.binary_location = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

# Inicia el navegador
driver = webdriver.Chrome(options=chrome_options)

# Abre la página de interés
driver.get("https://www.udemy.com/course/django-angular/learn/lecture/29066410#overview")

# Espera un tiempo para que la página se cargue completamente (ajusta según sea necesario)
driver.implicitly_wait(10)

# Obtiene las solicitudes de red
obtener_recursos()

# Cierra el navegador cuando hayas terminado
driver.quit()
