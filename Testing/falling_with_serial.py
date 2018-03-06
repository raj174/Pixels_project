import opc
import time
import random
import colorsys
import serial

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
    j = serial.readline().replace('\r\n','').split(' ')
    j = map(float,j)
    return j

def fade_out(prev_pixel,fade_time):                                         #from full bright to dim and full bright
    pixels = prev_pixel
    new_pixels = []
    for i in range(len(pixels)):                                            #for every LED takes the previous colour and gives it full brightness
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
    while brightness > 0:                                                   #slowly decreases the brightness
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
                while (time.time() - start_time) < 3:
                    if loop >20:
                        break
                    else:
                        j = get_serial(serial_device)
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
            pixels = [(0,0,0)] * (num)
            pixels[i] = current_colour
            pixels  = pixels + new
            client.put_pixels(pixels*6)
            time.sleep(0.01)
        addition.append(current_colour)
        new = list(addition)
        new.reverse()
        num = num -1
    fade_out(pixels*6,0.1)

serial_device = None
try:
    serial_device = serial.Serial('COM6', 9600)                                           #comment out if no arduino,make sure COM port is correct 
except:
    print 'No arduino detected'
    serial_device = None
##h = 180
##current_colour = conv_hsv(h,100,100)
##client.put_pixels(initial_pixels*6)
##pixels = initial_pixels

client = opc.Client('localhost:7890')
falling(244 ,100 ,150)
