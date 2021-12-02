import requests
from bs4 import BeautifulSoup

urls = {'new brighton' : 'https://magicseaweed.com/New-Brighton-Beach-Surf-Report/5212/',
        'yaroomba' : 'https://magicseaweed.com/Yaroomba-Surf-Report/5362/',
        'south straddie' : 'https://magicseaweed.com/South-Stradbroke-Island-Surf-Report/1010/',
        'palm beach' : 'https://magicseaweed.com/Palm-Beach-Surf-Report/6140/',
        'noosa' : 'https://magicseaweed.com/Tea-Tree-Noosa-Surf-Report/544/'}

def get_swell(location):
    url = urls[location]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lis  = soup.findAll('li')
    for li in lis:
        if li.has_attr( "class" ) and li["class"] == ['rating-text', 'text-dark']:
                return li.text.strip()

def get_wind(location):
    url = urls[location]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    divs  = soup.findAll('div')
    for div in divs:
        if div.has_attr("data-original-title"):
                return div["data-original-title"].strip()

class Conditions:
    def __init__(self, location):
        self.location = location
        self.swell = get_swell(location)
        self.wind = get_wind(location)

location = input("enter location: ")
if location in urls:
    data = Conditions(location)
    print(f"swell: {data.swell}")
    print(f"wind: {data.wind}")