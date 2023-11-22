from seleniumwire import webdriver
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
import requests


def iniciar_sesion():
    driver.implicitly_wait(3)
    driver.get("https://www.udemy.com/join/login-popup")
    email = driver.find_element(by=By.NAME, value="email")
    contra = driver.find_element(by=By.NAME, value="password")
    pressContinuar = driver.find_element(by=By.XPATH, value="//button[contains(@class, 'ud-btn ud-btn-large ud-btn-brand ud-heading-md helpers--auth-submit-button--2K2dh')]")

    email.send_keys("waltergaraycr@gmail.com")
    contra.send_keys("david@2004")

    pressContinuar.click()
    time.sleep(2)

def get_recursos(url):
    time.sleep(3)
    driver.get(url)
    solicitudes = driver.requests
    for solicitud in solicitudes:
        if solicitud.response:
            print('URL del recurso:', solicitud.url)
            content_type_header = solicitud.response.headers.get('content-type', 'No se encontró la cabecera Content-Type')
            print('Tipo de recurso:', content_type_header)
            print('--------------')

# Inicia el navegador
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

chrome_options = webdriver.ChromeOptions()

chrome_options.binary_location = chrome_path
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Superar cloudfare
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.udemy.com")

time.sleep(3)



# Cierra el navegador
driver.quit()
