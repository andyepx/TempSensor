#!/usr/bin/python

# FROM: https://raw.githubusercontent.com/adafruit/Adafruit_Python_DHT/master/examples/google_spreadsheet.py

# AIzaSyD4LhIjKMSx01Axq5wqKYrVYWf6uLDDGfI

import json
import sys
import time
import datetime

import Adafruit_DHT

from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

scopes = ['https://www.googleapis.com/auth/fusiontables']

credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scopes=scopes)
http_auth = credentials.authorize(Http())

print http_auth

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN = 22

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS = 60

while True:

    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity is None or temp is None:
        time.sleep(2)
        continue

    print('Temperature: {0:0.1f} C'.format(temp))
    print('Humidity:    {0:0.1f} %'.format(humidity))

    t = '{0:0.1f}'.format(temp)
    h = '{0:0.1f}'.format(humidity)
    dt = datetime.datetime
    d = str(dt.year) + '-' + str(dt.month) + '-' + str(dt.date) + ' ' + \
        str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)

    query = 'INSERT INTO 15LQJP48AhfQ2jlLkQrykrBUmnJqSCjdCr8hvLguz ' \
            '(Date, Temperature, Humidity) VALUES (\"' + d + '\",' + t + ', ' + h + ')'

    print query

    resp, content = http_auth.request(
        uri='https://www.googleapis.com/fusiontables/v2/query',
        method='POST',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        body='sql='+query,
    )

    print content

    # Wait 30 seconds before continuing
    time.sleep(FREQUENCY_SECONDS)
