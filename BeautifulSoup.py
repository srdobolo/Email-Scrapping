from bs4 import BeautifulSoup
import requests, re

email_id = re.compile('\w+@\w+.\w+')
html = requests.get('https://netemprego.com/view.php?job_id=2010610&auth_sess=e2t7rcudbcepcub7fsja4slbvr&ref=1e73e70e9b7894247ffa7f4d7').text
soup = BeautifulSoup(html, 'html.parser')
emails = soup.find_all(text=email_id)

for email in emails:
    print(email)
    


