import opc
import time
import random
import colorsys

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

def fade_out(prev_pixel,fade_time):               #from full bright to dim and full bright
    pixels = prev_pixel
    new_pixels = []
    for i in range(len(pixels)):                                #for every LED takes the previous colour and gives it full brightness
        if pixels[i] == (0,0,0):
            new_val = (0,0,0)
            new_pixels.append(new_val)
            pass
        else:
            r,g,b = pixels[i]
            new_val = conv_rgb_hsv(r,g,b)
            h,s,v = new_val
            v = 0
            new_pixels.append(new_val)
            pixels[i] = conv_hsv(h,s,v)
    client.put_pixels(pixels)
    time.sleep(1)
    brightness = 0
    while brightness <= 100:                                #Slowly increases the brightness
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
        time.sleep(fade_time)
def stars(time_wanted):
    start_time1 = time.time()
    while (time.time() - start_time1) < time_wanted:
        leds = 360
        pixels = [ (0,0,0) ] * 360
        for j in range(6):                                              #Takes four random LED's from each strip and fades in and fade out
            rand = random.sample(range(0,60),4)
            for k in range(4):
                k = rand[k] +(j*60)
                pixels[k] = (255,218,54)
        fade_out(pixels,0.1)
        pixels = [(0,0,0,)] *360

client = opc.Client('localhost:7890')
stars(20)
