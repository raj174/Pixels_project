import serial
import opc
import time
import random
import colorsys

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



'''Need to connect the arduino 101 before running'''

#client = opc.Client('192.168.2.1:7890')
client = opc.Client('localhost:7890')

ser = serial.Serial('COM6', 9600)
val = True
prev_yaw = 0
initial_pitch = 0
initial_roll = 0
prev_pitch = 0
prev_roll = 0
loop = 0
h = 180
current_colour = conv_hsv(h,100,100)
pixel_no = 30
pixel_no2 = 29
initial_pixels = [ (0,0,0) ] * 29 +[current_colour] * 2 + [ (0,0,0) ] * 29
client.put_pixels(initial_pixels*6)
pixels = initial_pixels
while True:
    j = ser.readline().replace('\r\n','').split(' ')
    j = map(float,j)
    if loop >2000:
        loop = 0
    if val == True:                                                             #if its the first time get the new values
        prev_yaw,prev_pitch,prev_roll = j
        val = False
    yaw,pitch,roll = j
    if yaw - prev_yaw < 1:                                                      #only work if the change is greater than 1 as yaw is always increasing 
        if prev_yaw - yaw > 1:                                                  #if going to the right add the h
            if h == 360:
                pass
            else:
                h = h + 5
                for i in range(len(pixels)):                                    #if colour is black skip                                            
                    if pixels[i] == (0,0,0):
                        pass
                    else:
                        current_colour = conv_hsv(h,100,100)
                        pixels[i] = current_colour
        prev_yaw = yaw
    else:                                                                       #if going to the left subtract the h
        if h == 0:
            pass
        else:  
            h = h - 5
            for i in range(len(pixels)):                                            
                if pixels[i] == (0,0,0):
                    pass
                else:
                    current_colour = conv_hsv(h,100,100)
                    pixels[i] = current_colour
        prev_yaw = yaw
    if prev_pitch < 0 :                                                         #moving up from centre or origin
        if prev_pitch-pitch> 0.5:                                               #add led while moving up, by giving colour
            pixels[pixel_no2] = current_colour
            if pixel_no2 <= 0:
                pass
            else:
                pixel_no2 = pixel_no2 -1
        if prev_pitch - pitch < -0.5 :                                          #if moving down 
            pixels[pixel_no2] = (0,0,0)
            if pixel_no2 >= 30:
                pass
            else:
                pixel_no2 = pixel_no2 + 1
        prev_pitch = pitch
    else:                                                                       #same as above but moving down from centre or origin
        if prev_pitch - pitch < -0.5 :
            pixels[pixel_no] = current_colour
            if pixel_no == 59:
                pass
            else:
                pixel_no = pixel_no + 1
        if prev_pitch - pitch > 0.5 :
            pixels[pixel_no] = (0,0,0)
            if pixel_no <= 31:
                pass
            else:
                pixel_no = pixel_no -1
        prev_pitch = pitch
        
        
    client.put_pixels(pixels*6)
    loop = loop+1
    
    
    
