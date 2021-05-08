


# from pyowm import OWM
# #from pyowm.utils import config
# from pyowm.utils import timestamps

# owm = OWM('2fe092a70821d857336c4a91ef84636c')
# mgr = owm.weather_manager()


# # Search for current weather in London (Great Britain) and get details
# observation = mgr.weather_at_place('Ho Chi Minh,VN')
# w = observation.weather

# status = w.detailed_status         # 'clouds'
# temp = w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
# print(status)
# print(str(temp['temp']) + ' celcius')

# # Will it be clear tomorrow at this time in Milan (Italy) ?
# forecast = mgr.forecast_at_place('Milan,IT', 'daily')
# answer = forecast.will_be_clear_at(timestamps.tomorrow())


import requests
import json

api_key = '2fe092a70821d857336c4a91ef84636c'
#vĩ độ
lat = "10.823099"
#kinh độ
lon = "106.629662"
url = "http://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&units=metric&appid=%s" % (lat,lon,api_key)
response = requests.get(url)
data = json.loads(response.text)
# print(data)

temp = data['current']['temp']
print(str(temp)+' celcius')
status = data['current']['weather'][0]['description']
print(status)
icon = data['current']['weather'][0]['icon']
print(icon)