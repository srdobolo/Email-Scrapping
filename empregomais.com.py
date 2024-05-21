from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

data = []

# Function to perform actions for different values of x
def process_element(x):
    try:
        # Click on the oferta_link element
        oferta_link = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/section[2]/div/div/div[1]/div[{x}]/div/div/div[2]/div[1]/div[2]/a')))
        oferta_link.click()
        driver.refresh()
    except Exception as e:
        return
    
    try:
        # Click on the email_click element
        email_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="spoiler-email font-bold underline cursor-pointer"]')))
        email_click.click()
    except Exception as e:
        return driver.back()
    
    try:
        # Get the text content of the mail element
        mail = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="spoiler-email font-bold underline cursor-pointer"]')))
        mail_text = mail.text
        print(mail_text)
        data.append(mail_text)
    except Exception as e:
        return 
    
    try:
        # Click on the go_back element
        driver.back()
        driver.refresh()
    except Exception as e:
        return
    
    try:
        # Click on the go_back element
        go_back = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/div/main/div/div[1]/a')))
        go_back.click()
    except: 
        None

# Specify the path to the ChromeDriver executable
chrome_driver_path = 'chromedriver.exe'

# Specify the path to the Adblock Plus CRX file
adblock_path = 'Adblock Plus CRX.crx'

# Create Chrome options
chrome_options = Options()
chrome_options.add_extension(adblock_path)
chrome_options.add_argument("--disable-javascript")

# Create a Service object with the path to the ChromeDriver executable
service = Service(chrome_driver_path)

# Create a WebDriver instance with the Service object and Chrome options
driver = webdriver.Chrome(service=service, options=chrome_options)

# The URL you want to open
website = 'https://empregomais.com/'

# Open the website
driver.get(website)
wait = WebDriverWait(driver, 1)

# Iterate over values of x
while True:
    for x in range(1, 25):
        process_element(x)
    
    try:
        next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="next page-numbers"]')))
        next_page.click()
    except Exception as e:
        print(f"An error occurred while clicking the next page button: {e}")
        break  # Exit the loop if there is an issue clicking the next page button

# Close the WebDriver
driver.quit()

# Create a DataFrame and remove duplicates
df = pd.DataFrame({'email': data})
df = df.drop_duplicates()

# Export DataFrame to CSV file
df.to_csv('output.csv', index=False)
print("DataFrame has been exported to 'output.csv'")
