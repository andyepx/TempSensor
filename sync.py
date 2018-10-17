#!/usr/bin/python

# AIzaSyD4LhIjKMSx01Axq5wqKYrVYWf6uLDDGfI

import datetime

import requests
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/fusiontables']

credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scopes=scopes)
http_auth = credentials.authorize(Http())

g = requests.get("http://192.168.1.42/data")

data = g.json()

temperature = data['living_room']['temperature']
humidity = data['living_room']['humidity']
index = data['living_room']['index']

print('Temperature:             {0:0.1f} C'.format(temperature))
print('Humidity:                {0:0.1f} %'.format(humidity))
print('Temperature Index:       {0:0.1f} C'.format(index))

t = '{0:0.1f}'.format(temperature)
h = '{0:0.1f}'.format(humidity)
i = '{0:0.1f}'.format(index)
d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

query = 'INSERT INTO 1HB7eZqHjz4WA-zaPsu_MtfWCE61rhms-zbBoC02Y ' \
        '(Date, Temperature, Humidity, Index) VALUES (\'' + d + '\',' + t + ', ' + h + ', ' + i + ')'

print query

resp, content = http_auth.request(
    uri='https://www.googleapis.com/fusiontables/v2/query',
    method='POST',
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    body='sql=' + query,
)

print content
print resp
