from bs4 import BeautifulSoup
import requests, re

email_id = re.compile('\w+@\w+.\w+')
html = requests.get('SITE URL').text
soup = BeautifulSoup(html, 'html.parser')
emails = soup.find_all(text=email_id)

for email in emails:
    print(email)
    


