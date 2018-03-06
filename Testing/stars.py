import opc
import time
import random
import colorsys
import requests
import json
import pprint
from threading import Timer


def conv_rgb_hsv(r,g,b):
    rgb = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
    hsv = (int(rgb[0]*360.0), int(rgb[1]*100.0), int(rgb[2]*100.0))
    return hsv
def conv_hsv(h,s,v):
    hsv = colorsys.hsv_to_rgb(h/360.0,s/100.0,v/100.0)
    rgb = (int(hsv[0]*255.0), int(hsv[1]*255.0), int(hsv[2]*255.0))
    return rgb
def fade_inout(prev_pixel,no_of_times):               #from full bright to dim and full bright
    pixels = prev_pixel
    new_pixels = []
    for i in range(len(pixels)):
        if pixels[i] == (0,0,0):
            new_val = (0,0,0)
            new_pixels.append(new_val)
            pass
        else:
            r,g,b = pixels[i]
            new_val = conv_rgb_hsv(r,g,b)
            h,s,v = new_val
            v = 100
            new_pixels.append(new_val)
            pixels[i] = conv_hsv(h,s,v)
    client.put_pixels(pixels)
    time.sleep(1)
    for i in range(no_of_times):
        brightness = 100
        while brightness >= 0:
            brightness = brightness - 5
            for i in range(len(pixels)):
                if new_pixels[i] == (0,0,0):
                    pixels[i] = (0,0,0)
                    pass
                else:
                    h,s,v = new_pixels[i]
                    v = brightness
                    pixels[i] = conv_hsv(h,s,v)
            client.put_pixels(pixels)
            time.sleep(0.1)
        while brightness <= 100:
            brightness = brightness + 5
            for i in range(len(pixels)):
                if new_pixels[i] == (0,0,0):
                    pixels[i] = (0,0,0)
                    pass
                else:
                    h,s,v = new_pixels[i]
                    v = brightness
                    pixels[i] = conv_hsv(h,s,v)
            client.put_pixels(pixels)
            time.sleep(0.1)

def stars(time_wanted):
    start_time1 = time.time()
    while (time.time() - start_time1) < time_wanted:
        leds = 360
        pixels = [ (0,0,0) ] * 360
        for j in range(6):
            rand = random.sample(range(0,60),4)
            for k in range(4):
                k = rand[k] +(j*60)
                pixels[k] = (255,218,54)
        fade_inout(pixels,1)
        pixels = [(0,0,0,)] *360
    

client = opc.Client('localhost:7890')
        
stars(20)
