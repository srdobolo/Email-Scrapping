from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import sys
import html  # Import the html module to decode HTML entities
from ftfy import fix_text  # Import ftfy to fix encoding issues

sys.stdout.reconfigure(encoding='utf-8')

# Configurar opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar sem abrir o navegador
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Iniciar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL do feed RSS
feed_url = "https://feeds.feedburner.com/Net-empregos"
driver.get(feed_url)

time.sleep(3)  # Espera para garantir o carregamento da página

# Capturar o código-fonte e garantir a codificação correta
html_source = driver.page_source.encode("utf-8").decode("utf-8")
driver.quit()

# Processar com BeautifulSoup
soup = BeautifulSoup(html_source, "xml")  # XML para melhor parsing do RSS

# Extrair todas as ofertas de emprego
items = soup.find_all("item")

for item in items:
    title = item.find("title").text.strip()
    dc_creator = item.find("dc:creator").text.strip() if item.find("dc:creator") else "Sem autor"
    link = item.find("link").text.strip()
    description = item.find("description").text.strip() if item.find("description") else "Sem descrição"
    pub_date = item.find("pubDate").text.strip() if item.find("pubDate") else "Sem data"
    guid = item.find("guid").text.strip() if item.find("guid") else "Sem GUID"
    
    # Fix encoding issues using ftfy
    title = fix_text(title)
    dc_creator = fix_text(dc_creator)
    link = fix_text(link)
    description = fix_text(description)
    pub_date = fix_text(pub_date)
    guid = fix_text(guid)
    
    # Use BeautifulSoup to parse the description and extract clean text
    description_soup = BeautifulSoup(description, "html.parser")
    clean_description = description_soup.get_text(separator="\n")  # Use newlines for better readability
    
    print("Job Title:", title)
    print("Author:", dc_creator)
    print("Job Link:", link)
    print("Description:", clean_description)
    print("Post Date:", pub_date)
    print("GUID:", guid)
    print("-" * 50)