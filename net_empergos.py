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
# chrome_options.add_argument("--headless")  # Executar sem abrir o navegador
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
items = soup.find_all("item")[:10]  # Limitar a 10 para debug

for index, item in enumerate(items):
    print(f"Processando oferta {index + 1}/{len(items)}...")
    try:
        link = fix_text(item.find("link").text.strip())
        driver.get(link)
        time.sleep(5)  # Aguardar mais tempo para carregamento

        try:
            # Lidar com a cookie wall
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", cookie_button)
            cookie_button.click()
            time.sleep(2)  # Esperar para garantir que o botão de cookies seja clicado

            # Fechar o pop-up
            close_popup_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "sp-prompt-close"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", close_popup_button)
            close_popup_button.click()
            time.sleep(2)  # Esperar para garantir que o pop-up seja fechado

            # Localizar e clicar no botão "Mostrar Email"
            show_email_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "job-mail"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_email_button)
            show_email_button.click()
            time.sleep(3)  # Esperar para garantir que o email carregue

            # Extrair email
            email_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]"))
            )
            email = email_element.get_attribute("href").replace("mailto:", "").split("?")[0]
            print(f"Email encontrado: {email}")
        except Exception as e:
            print(f"Erro ao obter e-mail: {str(e)}")
    except Exception as e:
        print(f"Erro ao processar oferta {index + 1}: {str(e)}")

# Fechar o navegador
driver.quit()