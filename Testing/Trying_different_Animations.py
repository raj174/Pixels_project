import opc
import time
import colorsys

def conv_hsl(h,s,l):
    hls = colorsys.hls_to_rgb(h/360.0,s/100.0,l/100.0)
    hls = (
        int(hls[0]*255.0),
        int(hls[1]*255.0),
        int(hls[2]*255.0)
        )
    return hls

client = opc.Client('localhost:7890')



def rainbow(l,s):                                       #Displays a rainbow giving it lightness and saturation 
    rgb = []
    set_val = [] 
    for h in range(60):
        val = h * 6
        set_val.append(val)
        #print set_val
        #print val
        if h == 0:
            rgb = [conv_hsl(val,l,s)] 
        else:
            rgb = [conv_hsl(val,l,s)] + rgb
        client.put_pixels(rgb)
        time.sleep(.01)
    while True:
        rgb_new = []
        for i in range(60):
            rgb_new = [conv_hsl(set_val[i],l,s)] + rgb_new
            rgb[0:i+1] = rgb_new
            #print new
            #rgb[i] = new
            #print rgb
            client.put_pixels(rgb)
            time.sleep(.01)
    return

rainbow(50,50)
#client.put_pixels(rgb)

