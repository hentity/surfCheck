# scraping libraries
import requests
from bs4 import BeautifulSoup

# regex
import re

# urls for each of the locations
urls = {'new brighton' : 'https://magicseaweed.com/New-Brighton-Beach-Surf-Report/5212/',
        'yaroomba' : 'https://magicseaweed.com/Yaroomba-Surf-Report/5362/',
        'south straddie' : 'https://magicseaweed.com/South-Stradbroke-Island-Surf-Report/1010/',
        'palm beach' : 'https://magicseaweed.com/Palm-Beach-Surf-Report/6140/',
        'noosa' : 'https://magicseaweed.com/Tea-Tree-Noosa-Surf-Report/544/'}

# return the swell as a string for a given location
def get_swell(location):
    url = urls[location]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lis  = soup.findAll('li')
    for li in lis:
        if li.has_attr( "class" ) and li["class"] == ['rating-text', 'text-dark']:
                return li.text.strip()

# return wind as a string for a given location
def get_wind(location):
    url = urls[location]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    divs  = soup.findAll('div')
    for div in divs:
        if div.has_attr("data-original-title"):
            if div["data-component"] == "WIND":
                wind_string = div["data-original-title"].strip()
                break
    return Wind(wind_string)

class Wind:
    def __init__(self, wind_string):
        m = re.match(r"(?P<speed>.*)mph - (?P<strength>.*), (?P<direction>.*) - (?P<angle>.*)°", wind_string)
        self.speed = int(m.group('speed')) * 1.6
        self.strength = m.group('strength')
        self.direction = m.group('direction')
        self.angle = int(m.group('angle'))

# conditions class - will eventually have all relevant info on surf conditions
class Conditions:
    def __init__(self, location):
        self.location = location
        self.swell = get_swell(location)
        self.wind = get_wind(location)

# ask user for location
location = input("enter location: ")

# print swell and wind data for that location
if location in urls:
    data = Conditions(location)
    print(f"swell: {data.swell}")
    print(f"wind: {data.wind.speed}km/h, {data.wind.angle}°")