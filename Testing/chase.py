import colorsys
import opc
import time
def conv_hsv(h,s,v):
    hsv = colorsys.hsv_to_rgb(h/360.0,s/100.0,v/100.0)
    rgb = (int(hsv[0]*255.0), int(hsv[1]*255.0), int(hsv[2]*255.0))
    return rgb

def conv_rgb_hsv(r,g,b):
    rgb = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
    hsv = (int(rgb[0]*360.0), int(rgb[1]*100.0), int(rgb[2]*100.0))
    return hsv


def chase2(sleep_time,run_time):                                        #option 1
    numLED = 180
    addition = []
    j = 0
    black = [(0,0,0)]
    pixels = black * 180
    start_time = time.time()
    while (time.time() - start_time) < run_time:                                              
        h = 0 
        for i in range(j*3+3):                                          #gives the last few pixels the colou 
            addition =  [conv_hsv(h,70,70)] + addition
            pixels = [conv_hsv(h,70,70)] + pixels
            pixels = pixels[:-1]
            old = list(addition)
            if numLED-3-(j*3) < 0:
                old.reverse()
                print old
                pixels = pixels + pixels[:-1]+old
                client.put_pixels(pixels)    
            else:
                client.put_pixels(pixels*2)
            time.sleep(sleep_time)
            if h >=360:
                h = 0
            h = h + 2
        for i in range(numLED-3-(j*3)):
            pixels = black*(i+1)+ addition + black * (numLED-(j*3+3)-(1+i))
            client.put_pixels(pixels*2)
            time.sleep(sleep_time)
        addition = []
        j = j+1
    fade_out(pixels*2,0.1)
        
def chase2_v2(v,sleep_time,run_time):                                      #option 2
    numLED = 180
    addition = []
    black = [(0,0,0)]
    pixels = black * 180
    start_time = time.time()
    while (time.time() - start_time) < run_time:                                              
        for j in range(numLED):
            h = 0
            for i in range(j*3+3):                                              #makes a list of led in multiples of three 
                addition =  [conv_hsv(h,70,v)] + addition
                pixels = [conv_hsv(h,70,v)] + pixels
                pixels = pixels[:-1]
                client.put_pixels(pixels*2)
                time.sleep(sleep_time)
                h = h + 2
            for i in range(numLED-3-(j*3)):
                pixels = black*(i+1)+ addition + black * (numLED-(j*3+3)-(1+i))
                client.put_pixels(pixels*2)
                time.sleep(sleep_time)
            addition = []
    fade_out(pixels,0.1)
client = opc.Client('192.168.2.1:7890')
chase2_v2(90,0.0001,100)
