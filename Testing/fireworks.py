import opc
import time
import random
import colorsys
import requests
import json
import pprint
from threading import Timer

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

def fade_out(prev_pixel,fade_time):                             #from dim to full bright and full bright
    pixels = prev_pixel
    new_pixels = []
    for i in range(len(pixels)):                                #for every LED takes the previous colour and gives it full brightness
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
    #time.sleep(1)
    brightness = 0
    while brightness <= 100:                                    #Slowly increases the brightness
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
    return pixels
def fade_in(prev_pixel,fade_time):                              #from full bright to dim and full bright
    pixels = prev_pixel
    new_pixels = []
    for i in range(len(pixels)):                                #for every LED takes the previous colour and gives it full brightness
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
    #time.sleep(1)
    brightness = 100
    while brightness >= 0:                                      #slowly decreases the brightness
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
    return pixels
        
def fireworks():
    for j in range(6):
        pixels = [(0,0,0)] * 60
        range_num = random.randrange(5,15,1)
        new_pixels = []
        b = 100
        time_rest = 0.01
        for i in range(range_num):
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
        for i in range(loop):
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
        for i in range(rand_pixel):
            r,g,b = colour[number]
            h,s,v = conv_rgb_hsv(r,g,b)
            s = s - i*2
            v = v - i*(100/rand_pixel)
            rgb = conv_hsv(h,s,v)
            sparkle.append(rgb)
        #for 
        pixels = j*60*[(0,0,0)]+sparkle
        fade_out(pixels,0.01)
        fade_in(pixels,0.1)
client = opc.Client('localhost:7890')
fireworks()


##def fireworks2():
##    for j in range(2):
##        pixels = [(0,0,0)] * 60
##        for k in range(3):
##            range_num = random.randrange(5,15,1)
##            new_pixels = []
##            b = 100
##            time_rest = 0.01
##            for i in range(range_num):
##                rgb = conv_hsv(36,75,b)
##                pixels[59-i] = rgb
##                new_pixels.append(rgb)
##                b = b - 5
##                prev_pixels = pixels
##                pixels = j*60*[(0,0,0)]+pixels
##                client.put_pixels(pixels)
##                pixels = prev_pixels
##                time.sleep(time_rest)
##            
##        loop = 60 - range_num
##        for i in range(loop):
##            pixels = [ (0,0,0) ] * 60
##            pixels = pixels[0:(loop-i-1)] + new_pixels+[(0,0,0)]*(i+1)
##            prev_pixels = pixels
##            pixels = j*60*[(0,0,0)]+pixels
##            client.put_pixels(pixels)
##            pixels = prev_pixels
##            time.sleep(time_rest)
##            time_rest = time_rest + 0.0001
##        number = random.randrange(0,3,1)
##        colour = [ (255,0,0),(0,255,0),(0,0,255) ]
##        pixels = [(0,0,0)] * (60+(j*60))
##        client.put_pixels(pixels)
##        rand_pixel = random.randrange(20,36,1)
##        sparkle = []
##        for i in range(rand_pixel):
##            r,g,b = colour[number]
##            h,s,v = conv_rgb_hsv(r,g,b)
##            s = s - i*2
##            v = v - i*(100/rand_pixel)
##            rgb = conv_hsv(h,s,v)
##            sparkle.append(rgb)
##        pixels = j*60*[(0,0,0)]+sparkle
##        fade_out(pixels,0.01)
##        fade_in(pixels,0.1)
##    
#client = opc.Client('192.168.2.1:7890')



