import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from ftfy import fix_text

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

# Processar com BeautifulSoup
soup = BeautifulSoup(html_source, "xml")  # XML para melhor parsing do RSS

# Extrair todas as ofertas de emprego
items = soup.find_all("item")

for item in items:
    title = fix_text(item.find("title").text.strip())
    dc_creator = fix_text(item.find("dc:creator").text.strip()) if item.find("dc:creator") else "Sem autor"
    link = fix_text(item.find("link").text.strip())
    description = fix_text(item.find("description").text.strip()) if item.find("description") else "Sem descrição"
    pub_date = fix_text(item.find("pubDate").text.strip()) if item.find("pubDate") else "Sem data"
    guid = fix_text(item.find("guid").text.strip()) if item.find("guid") else "Sem GUID"

    # Acessar página da oferta de emprego
    driver.get(link)
    time.sleep(3)  # Aguarde o carregamento da página

    try:
        # Esperar até que o ícone do envelope esteja visível e clicar
        envelope_icon = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fa-envelope"))
        )
        envelope_icon.click()
        
        # Esperar o e-mail aparecer e extrair o link "mailto"
        email_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]")
        ))
        email = email_element.get_attribute("href").replace("mailto:", "").split("?")[0]
    except:
        email = "Não encontrado"
    
    # Print para debug
    print("Job Title:", title)
    print("Author:", dc_creator)
    print("Job Link:", link)
    print("Description:", description)
    print("Post Date:", pub_date)
    print("GUID:", guid)
    print("Email:", email)
    print("-" * 50)

# Fechar o navegador
driver.quit()

print("Scraping concluído!")
