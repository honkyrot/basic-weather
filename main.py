# weather data project from weather.gov's API
# them plot them with plotly

# imports
import requests
import json
import pandas as pd
import plotly.express as px
# example city used will be Fort Wayne, Indiana for this project
# with weather station NWS Forecast Office, Northern Indiana (IWX)

# test if API is active

def test_api():
    url = 'https://api.weather.gov/'
    response = requests.get(url)
    if response.status_code == 200:
        print('API is active')
    else:
        raise Exception('API is not active')
    
# test_api()

# then get the data



class WeatherData:

    def __init__(self):
        self.grid_x = None
        self.grid_y = None
        self.weather_data = None

    def start(self):
        """start the program"""
        self.get_gridpoint_data()
        self.get_data()
        self.present_data()

    def get_gridpoint_data(self):
        """Gets gridpoint data from weather.gov"""
        print("getting gridpoint data")

        url = 'https://api.weather.gov/points/41.0793,-85.1394' # the example city
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # print(data)

            self.grid_x = int(data['properties']['gridX'])
            self.grid_y = int(data['properties']['gridY'])

        return response.status_code


    def get_data(self):
        print("getting data")

        if self.grid_x is None or self.grid_y is None:
            raise Exception('Gridpoint data not found')

        url = f'https://api.weather.gov/gridpoints/IWX/{self.grid_x},{self.grid_y}/forecast?units=us'
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.weather_data = data

            # print(data)
        
        return response.status_code

    def present_data(self):
        print("presenting data")
        if self.weather_data is None:
            raise Exception('Weather data not found')

        df = pd.DataFrame(self.weather_data['properties']['periods'])
        df['startTime'] = pd.to_datetime(df['startTime'])
        df['endTime'] = pd.to_datetime(df['endTime'])

        print(df)

        fig = px.line(df, x='startTime', y='temperature')
        fig.show()

weather = WeatherData()
weather.start()
