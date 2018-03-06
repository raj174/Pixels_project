#!/usr/bin/env python

'''Main file for Submission, Has a few different animations that run depending on sunruse and sunset.'''

import opc
import time
import random
import colorsys
import requests
import json
import pprint
import serial
from threading import Timer

'''Running Automatically'''
def dayTime_Check():
    global dayTime
    global nightTime
    global current_time_sec
    j = Timer(300, dayTime_Check)
    j.start()
    current_time = time.ctime()[11:19].split(':')                               #Gets the current time and splits them
    current_time = map(int,current_time)
    current_time_sec = (current_time[0]*60*60) + (current_time[1]*60) + current_time[2]
    if current_time_sec <= 300 :
        get_API()                                                               #only if the computer is connected to the internet
    if current_time_sec < sunrise_sec or current_time_sec > sunset_sec:
        dayTime = 0
        nightTime = 1
    else:
        nightTime = 0
        dayTime = 1

def get_API():                                                                  #cant use if there is no internet connection
    global sunrise_sec
    global sunset_sec
    request = None
    try:
        request = requests.get('http://api.sunrise-sunset.org/json?lat=51.590396&lng=-0.230467&date=today')
    except:
        pass
    if request == None:
        file = open("newfile.txt", "r")
        j = file.read( ).split(':')
        print j
        sunrise_sec = int(j[1])
        sunset_sec = int(j[3])
        file.close()
    else:
        result = json.loads(request.content)
        #pprint.pprint(result)
        sunrise = result['results']['sunrise'].replace(' AM','').split(':')     #get value from dictionary,remove the unwanted characters,split the numbers to get hours minutes and sec
        sunset = result['results']['sunset'].replace(' PM','').split(':')
        sunrise = map(int,sunrise)                                              #convert to int
        sunset = map(int,sunset)

        sunrise_sec = (sunrise[0]*60*60) + (sunrise[1]*60) + sunrise[2]         #changing time to sec
        sunset_sec = (sunset[0]*60*60) + (sunset[1]*60) + sunset[2] + (60*60*12)

'''Usable functions for animation'''
def conv_hsl(h,l,s):
    hls = colorsys.hls_to_rgb(h/360.0,l/100.0,s/100.0)
    rgb = (int(hls[0]*255.0), int(hls[1]*255.0), int(hls[2]*255.0))
    return rgb

def conv_hsv(h,s,v):
    hsv = colorsys.hsv_to_rgb(h/360.0,s/100.0,v/100.0)
    rgb = (int(hsv[0]*255.0), int(hsv[1]*255.0), int(hsv[2]*255.0))
    return rgb

def conv_rgb_hsv(r,g,b):
    rgb = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
    hsv = (int(rgb[0]*360.0), int(rgb[1]*100.0), int(rgb[2]*100.0))
    return hsv

def conv_rgb_hsl(r,g,b):
    rgb = colorsys.rgb_to_hsl(r/255.0,g/255.0,b/255.0)
    hsl = (int(rgb[0]*360.0), int(rgb[1]*100.0), int(rgb[2]*100.0))
    return hsl

def get_serial(serial):
    if serial == None:
        return 'None'
    j = serial.readline().replace('\r\n','').split(' ')
    j = map(float,j)
    return j

def fade_in(prev_pixel,fade_time):                                              #from dim to full bright and full bright
    pixels = prev_pixel
    new_pixels = []
    for i in range(len(pixels)):                                                #for every LED takes the previous colour and gives it full brightness
        if pixels[i] == (0,0,0):
            new_val = (0,0,0)
            new_pixels.append(new_val)
        else:
            r,g,b = pixels[i]
            new_val = conv_rgb_hsv(r,g,b)
            h,s,v = new_val
            v = 0
            new_pixels.append(new_val)
            pixels[i] = conv_hsv(h,s,v)
    client.put_pixels(pixels)
    brightness = 0
    while brightness < 100:                                                     #Slowly increases the brightness
        brightness = brightness + 5
        for i in range(len(pixels)):
            if new_pixels[i] == (0,0,0):
                pixels[i] = (0,0,0)
            else:
                h,s,v = new_pixels[i]
                v = brightness
                pixels[i] = conv_hsv(h,s,v)
        client.put_pixels(pixels)
        time.sleep(fade_time)

def fade_out(prev_pixel,fade_time):                                             #from full bright to dim and full bright
    pixels = prev_pixel
    new_pixels = []
    for i in range(len(pixels)):                                                #for every LED takes the previous colour and gives it full brightness
        if pixels[i] == (0,0,0):
            new_val = (0,0,0)
            new_pixels.append(new_val)
        else:
            r,g,b = pixels[i]
            new_val = conv_rgb_hsv(r,g,b)
            h,s,v = new_val
            v = 100
            new_pixels.append(new_val)
            pixels[i] = conv_hsv(h,s,v)
    client.put_pixels(pixels)
    brightness = 100
    while brightness > 0:                                                       #slowly decreases the brightness
        brightness = brightness - 5
        for i in range(len(pixels)):
            if new_pixels[i] == (0,0,0):
                pixels[i] = (0,0,0)
            else:
                h,s,v = new_pixels[i]
                v = brightness
                pixels[i] = conv_hsv(h,s,v)
        client.put_pixels(pixels)
        time.sleep(fade_time)

'''Animation Functions'''

def blinkLED(time_wanted):                       
    numLED = 360
    black = [ (0,0,0) ] * numLED
    start_time = time.time()                                                    # remember when started
    while (time.time() - start_time) < time_wanted:                             # check if the required time has passed
        all_pixels = [ (random.randrange(0,255,1),random.randrange(0,255,1),100) ] * numLED
        client.put_pixels(black)
        time.sleep(0.1)
        client.put_pixels(all_pixels)
        time.sleep(0.1)

#Blinks odd and even Led's        
def blink_OtherLED(time_wanted):
    numLED = 360
    black = [ (0,0,0) ] * numLED
    start_time1 = time.time()   
    while (time.time() - start_time1) < time_wanted:
        colour = [ (random.randrange(0,255,1),
                    random.randrange(0,255,1),
                    random.randrange(0,255,1)),
                   (0,0,0)                      ] * (numLED/2)
        colour2 = [ (0,0,0),
                    (random.randrange(0,255,1),
                     random.randrange(0,255,1),
                     random.randrange(0,255,1)) ] * (numLED/2)
        client.put_pixels(black)
        time.sleep(.2)
        client.put_pixels(colour)
        time.sleep(.2)
        client.put_pixels(black)
        time.sleep(.2)
        client.put_pixels(colour2)
        time.sleep(.2)
        
#Changes colour as you go through the loop
def chase(no_of_loops):                                       
    loop = 0
    h = 0
    numLED = 180
    num = 180
    addition = []
    new = []
    while loop < no_of_loops:                                              
        for j in range(numLED):
            for i in range(numLED):                                             #go one by one to the 180th led, then start again with a new colour
                pixels = [ (0,0,0) ] * numLED
                pixels[i] = conv_hsv(h,70,70)
                pixels = pixels+new
                client.put_pixels(pixels*2)
                time.sleep(0.008)
            addition.append(conv_hsv(h,70,70))
            new = list(addition)                                                #remember the colour, so you can add it at the end
            new.reverse()
            numLED = numLED-1
            h = h + 2
        pixels = pixels*2
        fade_out(pixels,0.1)
        loop = loop+1

#Adds more led of different colour every time it finishes a cycle
def chase2(v,sleep_time,run_time):
    numLED = 180
    addition = []
    j = 0
    black = [(0,0,0)]
    pixels = black * 180
    start_time = time.time()
    while (time.time() - start_time) < run_time:                                              
        h = 0 
        for i in range(j*3+3):                                                  #initiates led in multiple of three
            addition =  [conv_hsv(h,70,v)] + addition
            pixels = [conv_hsv(h,70,v)] + pixels
            pixels = pixels[:-1]                                                #removes the last led to get the effect of continuing in the top
            client.put_pixels(pixels*2)
            time.sleep(sleep_time)
            if h >=360:
                h = 0
            h = h + 2
        for i in range(numLED-3-(j*3)):                                         #moves the led to its destination
            pixels = black*(i+1)+ addition + black * (numLED-(j*3+3)-(1+i))
            client.put_pixels(pixels*2)
            time.sleep(sleep_time)
        addition = []
        j = j+1
    fade_out(pixels*2,0.1)
        
#Goes through the LED's one by one on the no of strips specified and at the end, the last one in the loop keeps on lighting up
#If the arduino is connected you can select the colour before it moves
def falling(r ,g ,b):                                 
    num = 60
    val = True
    prev_yaw = 0
    new = []
    addition = []
    current_colour = (r,g,b)
    h,s,v = conv_rgb_hsv(r,g,b)
    for j in range(num):
        start_time = time.time()
        loop = 0
        for i in range(num):
            if serial_device == None:
                pass
            else:
                while (time.time() - start_time) < 3:                           #Wait while the colour changes
                    if loop >20:
                        break
                    else:
                        j = get_serial(serial_device)                           #get values from the arduino and change colour
                        pixels = [(0,0,0)] * (num)
                        pixels  = pixels + new
                        if val == True:
                            prev_yaw,prev_pitch,prev_roll = j
                            val = False
                        yaw,pitch,roll = j
                        if yaw - prev_yaw < 1:
                            if prev_yaw - yaw > 1:
                                if h == 360:
                                    pass
                                else:
                                    h = h + 5                                           
                                    current_colour = conv_hsv(h,s,v)
                                loop = 0
                            loop = loop + 1
                            prev_yaw = yaw
                        else:
                            if h == 0:
                                pass
                            else:  
                                h = h - 5
                                current_colour = conv_hsv(h,s,v)
                            loop = 0
                            prev_yaw = yaw
                    pixels[0] = current_colour
                    client.put_pixels(pixels*6)
            pixels = [(0,0,0)] * (num)                                          #move the first row of led's
            pixels[i] = current_colour
            pixels  = pixels + new
            client.put_pixels(pixels*6)
            time.sleep(0.01)
        addition.append(current_colour)
        new = list(addition)
        new.reverse()                                                           #reversed so that append adds the new tuple at the end
        num = num -1
    fade_out(pixels*6,0.1)


#Displays a rainbow giving it lightness and saturation 
def rainbow(time_wanted,l,s, no_of_strips,back_and_forth = None):
    start_time = time.time()
    rgb = []
    set_val = []
    for h in range(60):
        val = h * 6
        set_val.append(val)
        if h == 0:
            rgb = [ conv_hsl(val,l,s) ]
        else:
            rgb = [conv_hsl(val,l,s)] + rgb
        
        addition = [(0,0,0)]*(59-h)                                             #addition implimented so that all strips glows in the same time
        prev_rgb = rgb
        rgb = rgb+addition
        client.put_pixels(rgb*no_of_strips)
        time.sleep(.1)
        rgb = prev_rgb
    while (time.time() - start_time) < time_wanted:
        rgb_new = []
        for i in range(60):                                                     #use just this for loop 
            rgb_new = [conv_hsl(set_val[i],l,s)] + rgb_new
            rgb[0:i+1] = rgb_new
            client.put_pixels(rgb*no_of_strips)
            time.sleep(.03)
        if back_and_forth ==1:
            rgb_new = []
            for j in range(60):                                                 #add this to previous if you want back and forth
                rgb_new = rgb_new+[conv_hsl(set_val[j],l,s)] 
                rgb[60-(j+1):60] = rgb_new
                client.put_pixels(rgb*no_of_strips)
                time.sleep(.03)
    fade_out(rgb*no_of_strips,0.1)


#Lights random LED's with random colours and randomly switches them off
def random_position(no_of_strips):
    leds = no_of_strips*60
    j = random.sample(range(0,leds),leds)                                       #gets a list of random no to follow
    pixels = [ (0,0,0) ] * leds
    new_pixels = []
    old_pixel = []
    for i in range(leds):                                                       #starts to switch on LED's in a random sequence
        i = j[i]                                                                #changes i to the random no from j
        pixels[i] = (random.randrange(0,255,10),
                     random.randrange(0,255,10),
                     random.randrange(0,255,10))
        client.put_pixels(pixels)
        time.sleep(0.1)
    old_pixel = list(pixels)
    fade_out(pixels,0.1)
    fade_in(old_pixel,0.1)
    k = random.sample(range(0,leds),leds)                                       #starts to switch off LED's in a random sequence
    for i in range(leds):
        i = k[i]
        old_pixel[i] = (0,0,0)
        client.put_pixels(old_pixel)
        time.sleep(0.1)

# fades in and out the leds in random position
def stars(time_wanted):
    start_time1 = time.time()
    while (time.time() - start_time1) < time_wanted:
        pixels = [ (0,0,0) ] * 360
        for j in range(6):                                                      #Takes 7 random LED's from each strip
            rand = random.sample(range(0,60),7)
            for k in range(7):
                k = rand[k] +(j*60)
                pixels[k] = (255,218,54)
        fade_in(pixels,0.1)
        fade_out(pixels,0.1)

#starts in the bottom and then looks like a blast when the set of led reach the top
def fireworks():
    for j in range(6):
        pixels = [(0,0,0)] * 60
        range_num = random.randrange(5,15,1)
        new_pixels = []
        b = 100
        time_rest = 0.01
        for i in range(range_num):                                              #gives the last few pixels the colour 
            rgb = conv_hsv(36,75,b)
            pixels[59-i] = rgb
            new_pixels.append(rgb)
            b = b - 5
            prev_pixels = pixels
            pixels = j*60*[(0,0,0)]+pixels
            client.put_pixels(pixels)
            pixels = prev_pixels
            time.sleep(time_rest)
        loop = 60 - range_num
        for i in range(loop):                                                   #moves the lighted up led's forward
            pixels = [ (0,0,0) ] * 60
            pixels = pixels[0:(loop-i-1)] + new_pixels+[(0,0,0)]*(i+1)
            prev_pixels = pixels
            pixels = j*60*[(0,0,0)]+pixels
            client.put_pixels(pixels)
            pixels = prev_pixels
            time.sleep(time_rest)
            time_rest = time_rest + 0.0001
        number = random.randrange(0,3,1)
        colour = [ (255,0,0),(0,255,0),(0,0,255) ]
        pixels = [(0,0,0)] * (60+(j*60))
        client.put_pixels(pixels)
        rand_pixel = random.randrange(20,36,1)
        sparkle = []
        for i in range(rand_pixel):                                             #get the explosion colours
            r,g,b = colour[number]
            h,s,v = conv_rgb_hsv(r,g,b)
            s = s - i*2
            v = v - i*(100/rand_pixel)
            rgb = conv_hsv(h,s,v)
            sparkle.append(rgb)
        #for 
        pixels = j*60*[(0,0,0)]+sparkle
        fade_in(pixels,0.01)
        fade_out(pixels,0.1)

'''Main Code'''

#client = opc.Client('192.168.2.1:7890')
client = opc.Client('localhost:7890')

'''Run to get the Animation change automatically for day and night'''
get_API()
serial_device = None
try:
    serial_device = serial.Serial('COM6', 9600)                                 #make sure COM port is correct 
except:
    print 'No arduino detected'
    serial_device = None

dayTime_Check()
while True:
    while nightTime == 1:
        '''put Night animations here'''
        blinkLED(10)
        chase(1)
        rainbow(10,60,60,6,1)
        random_position(6)
        chase2(60,0.01,150)
        stars(20)
        rainbow(30,60,60,6)
        fireworks()


    while dayTime == 1:
        '''put Day animations here'''
        blink_OtherLED(10)
        rainbow(20,60,60,6,1)
        chase2(95,0.0001,80)
        falling(random.randrange(0,255,1), random.randrange(0,255,1), random.randrange(0,255,1))
        chase2(95,0.001,80)
        random_position(6)
        chase(1)
        fireworks()

