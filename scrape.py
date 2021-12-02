import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://magicseaweed.com/New-Brighton-Beach-Surf-Report/5212/'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

lis  = soup.findAll('li')

for li in lis:
    if li.has_attr( "class" ) and li["class"] == ['rating-text', 'text-dark']:
            print(li.text.strip())