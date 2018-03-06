import time
import requests
import json
import pprint



#get data from api (current lat and long is near rittherman building)
request = requests.get('http://api.sunrise-sunset.org/json?lat=51.590396&lng=-0.230467&date=today')
result = json.loads(request.content)
#pprint.pprint(result)



sunrise = result['results']['sunrise'].replace(' AM','').split(':')     #get value from dictionary,remove the unwanted characters,split the numbers to get hours minutes and sec
sunset = result['results']['sunset'].replace(' PM','').split(':')
sunrise = map(int,sunrise)                                              #convert to int
sunset = map(int,sunset)

sunrise_sec = (sunrise[0]*60*60) + (sunrise[1]*60) + sunrise[2]         #changing time to sec
sunset_sec = (sunset[0]*60*60) + (sunset[1]*60) + sunset[2] + (60*60*12)
        
file = open("newfile.txt", "w")
file.write('sunrise_sec:'+ str(sunrise_sec)+':'+'sunset_sec:' + str(sunset_sec)) 
file.close()

