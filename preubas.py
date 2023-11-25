from selenium import webdriver
import json, os, time

chrome_options = webdriver.ChromeOptions()
settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }

prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    'savefile.default_directory': r"C:\Users\Usuario\Desktop\udemy-video-downloader\Course- Django, Postgres y Angular - Integracion Fullstack - Udemy (2)",
    'savefile.filename_prefix': "david.pdf"
}

chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument('--enable-print-browser')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://google.com")
nombre_pdf = ""
driver.execute_script('document.title = "' + nombre_pdf + '"; window.print();')
time.sleep(3)
driver.quit()