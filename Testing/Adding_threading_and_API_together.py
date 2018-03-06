import opc
import time
import random
import colorsys
import requests
import json
import pprint
from threading import Timer

def dayTime_Check():
    global dayTime
    global nightTime
    j = Timer(5, dayTime_Check)
    j.start()
    print 'going through loop'
    current_time = time.ctime()[11:19].split(':')
    current_time = map(int,current_time)
    current_time_sec = (current_time[0]*60*60) + (current_time[1]*60) + current_time[2]
    if current_time_sec <= 300 :
        get_API()
    if current_time_sec < sunrise_sec or current_time_sec > sunset_sec:
        dayTime = 0
        nightTime = 1
    else:
        nightTime = 0
        dayTime = 1


def get_API():
    global sunrise_sec
    global sunset_sec
    request = requests.get('http://api.sunrise-sunset.org/json?lat=51.590396&lng=-0.230467&date=today')
    result = json.loads(request.content)
    #pprint.pprint(result)
    sunrise = result['results']['sunrise'].replace(' AM','').split(':')     #get value from dictionary,remove the unwanted characters,split the numbers to get hours minutes and sec
    sunset = result['results']['sunset'].replace(' PM','').split(':')
    sunrise = map(int,sunrise)                                              #convert to int
    sunset = map(int,sunset)

    sunrise_sec = (sunrise[0]*60*60) + (sunrise[1]*60) + sunrise[2]         #changing time to sec
    sunset_sec = (sunset[0]*60*60) + (sunset[1]*60) + sunset[2] + (60*60*12)

#client = opc.Client('192.168.2.:7890')
client = opc.Client('localhost:7890')

get_API()
dayTime_Check()
while nightTime == 1:
    #put Night animations here
    print ('NIGHT')
while dayTime == 1:
    #put Day animations hereg
    print ('DAY')


