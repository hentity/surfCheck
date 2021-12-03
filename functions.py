import requests
from bs4 import BeautifulSoup
import csv
import re
import sys 

# ------CLASSES------

# contains information for a surf spot
class Spot:
    def __init__(self, name, url, angle):
        self.name = name
        self.url = url
        self.angle = int(angle)
        self.conditions = Conditions(self)
    def display_conditions(self):
        print("----------------")
        print(f"{self.name} current conditions: ")
        print(f"swell: {self.conditions.swell}")
        print(f"wind: {round(self.conditions.wind.speed, 1)}km/h {self.conditions.wind.direction}, {self.conditions.wind.angle}°")
        print("----------------")
    

# contains info about the wind (speed, direction)
class Wind:
    def __init__(self, wind_string):
        m = re.match(r"(?P<speed>.*)mph - (?P<strength>.*), (?P<direction>.*) - (?P<angle>.*)°", wind_string)
        self.speed = int(m.group('speed')) * 1.6
        self.strength = m.group('strength')
        self.direction = m.group('direction')
        self.angle = int(m.group('angle'))

# contains info about the conditions at a spot
class Conditions:
    def __init__(self, spot):
        self.spot = spot
        self.swell = fetch_swell(spot)
        self.wind = fetch_wind(spot)

# ------FUNCTIONS------

# return the swell as a string for a given spot
def fetch_swell(spot):
    url = spot.url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lis  = soup.findAll('li')
    for li in lis:
        if li.has_attr( "class" ) and li["class"] == ['rating-text', 'text-dark']:
                return li.text.strip()

# return wind as a string for a given spot
def fetch_wind(spot):
    url = spot.url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    divs  = soup.findAll('div')
    for div in divs:
        if div.has_attr("data-original-title"):
            if div["data-component"] == "WIND":
                wind_string = div["data-original-title"].strip()
                break
    return Wind(wind_string)

# read spots into dictionary from csv and webscrape data
def read_spots():
    spots = {}
    file = open('spots.csv')
    csvreader = csv.reader(file)
    print(f"\rfetching conditions...")
    for row in csvreader:
        spots[row[0]] = Spot(row[0], row[1], row[2])
    return spots

# browse spots and conditions
def browse(spots):
    while True:
        i = 1
        for spot in spots:
            print(f"[{i}] {spot}")
            i += 1
        selection = input("select spot, x to exit: ")
        if selection == "x":
            break
        elif not selection.isdigit():
            print("please enter a number")
            continue
        elif int(selection) < 1 or int(selection) > len(spots):
            print('invalid selection')
            continue
        else:
            selection = int(selection)
            selected_spot = spots[list(spots.keys())[selection - 1]]
            selected_spot.display_conditions()


