import requests
import math
import matplotlib.pyplot as plt
import numpy as np

api_key = '45e148639e7842faf878cf853a6e318b' #source API
location = 'christchurch' #location of beach
units = 'metric' #units
beach_face_direction = input("What direction does the beach face? ") #direction beach faces in degrees from vertical
longitude = 153.552444 #longitude of beach
latitude = -28.515525 #latitude of beach

def main():
    #wind, data = API_coordinates()
    wind, data = API_location()
    wind_direction, wind_speed = wind_decision(wind)
    x1, x2, y1, y2 = beach_plot(beach_face_direction)
    wind_plot(wind_direction, x1, x2, y1, y2, wind_speed)
    water_temp(data)

def API_location():
    '''Uses location name to source data from API'''
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}")
    data = response.json() #converting API to json script (from string)
    wind = data['wind'] #isolating wind data
    return wind, data

def API_coordinates():
    '''Uses geographic coordinates to source data from API'''
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units={units}")
    data = response.json() #converting API to json script (from string)
    wind = data['wind'] #isolating wind data
    
    return wind, data

def wind_decision(wind):
    '''Takes wind data and decides if it is on shore/off shore/across shore.
       (include acceptable wind ranges at some point pls dogg)
       Conditionals take wind direction and decide which way the wind is
       blowing relative to the beach.
    '''
    wind_speed = wind['speed'] #isolating wind speed from the API call
    wind_direction = wind['deg'] #isolating wind direction from the API call
    if float(beach_face_direction) - 45 <= wind_direction <= float(beach_face_direction) + 45:
        print("wind is on shore")
    elif float(beach_face_direction) + 135 <= wind_direction <= float(beach_face_direction) + 225:
        print("wind is off shore")
    else:
        print("wind is cross shore")
    gusts = wind['gust']
    print(f'wind speed is {wind_speed}km/h with gusts up to {gusts}km/h')
    print("(ideal wind conditions are less than 8mh/h and off shore)")
    return wind_direction, wind_speed

def water_temp(data):
    temperature = data['main']
    temp = [temperature['temp'], temperature['feels_like']]
    print(f'water temperature is {temp[0]} degrees but feels like {temp[1]} degrees')

def beach_plot(beach_face_direction):
    '''Plots direction the beach is facing
    '''
    x1 = 0 #reference x-value for beach
    y1 = 0 #reference y-value for beach
    if float(beach_face_direction) > 180:
        '''Direction the beach faces mirrors about the vertical axis. For
           simplicity, use only 0-180 degrees.'''
        beach_angle = math.radians(float(beach_face_direction) - 180)
    else:
        beach_angle = math.radians(float(beach_face_direction))
    x2 = x1 + math.cos(beach_angle)*10 #other end of beach x-value
    y2 = y1 + math.sin(beach_angle)*10 #other end of beach y-value
    x = [x1, -x2] #list of x-values for plotting
    y = [y1, y2] #list of y-values for plotting
    plt.plot(x, y) #plot of beach
    plt.xlim(-10, 10) #x-axis limits
    plt.ylim(0, 10) #y-axis limits
    return x1, x2, y1, y2
    
def wind_plot(wind_direction, x1, x2, y1, y2, wind_speed):
    '''Takes wind direction and magnitude and plots it against the beach
       direction
    '''
    x3 = 0 #starting x-value for wind
    y3 = (y2 - y1) / 2 #starting y-value for wind
    wind_angle = math.radians(float(wind_direction)) #conversion to radians
    x4 = x3 + math.cos(wind_angle)*float(wind_speed) #magnitude and direction of wind in x-direction
    y4 = y3 + math.sin(wind_angle)*float(wind_speed) #magnitude and direction of wind in y-direction
    x_ = [x3, x4] #list of x-values for plotting
    y_ = [y3, y4] #list of y-values for plotting
    x_head = [x3, x3 + math.cos(wind_angle+20)*float(wind_speed)/4], [x3, x3 + math.cos(wind_angle-20)*float(wind_speed)/4]
            #x-values for pointing arms of wind arrow
    y_head = [y3, y3 + math.sin(wind_angle+20)*float(wind_speed)/4], [y3, y3 + math.sin(wind_angle-20)*float(wind_speed)/4]
            #y-values for pointing arms of wind arrow
    plt.plot(x_, y_, 'red') #plot of direction and magnitude of wind
    plt.plot(x_head[0], y_head[0], 'red') #plot of left side of arrow head
    plt.plot(x_head[1], y_head[1], 'red') #plot of right side of arrow head
    
main()