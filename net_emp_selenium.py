from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configuração do ChromeDriver (substitua pelo caminho correto)
CHROMEDRIVER_PATH = 'chromedriver.exe'  # Atualize com o caminho correto

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Modo sem interface gráfica (opcional)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Inicializa o ChromeDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL do feed
feed_url = "https://feeds.feedburner.com/Net-empregos"

try:
    driver.get(feed_url)
    time.sleep(3)
    print(driver.page_source)  # Testa se está carregando a página corretamente
finally:
    driver.quit()