#!/usr/bin/env python
import opc
import time
import random
import colorsys

class DayTime(object):
    def __init__(self, client):
        self.black = (0,0,0)
        self.client = client
        self.counter = 0

    def update(self):
        if self.counter == 0:
            self.client.put_pixels( [self.black]*360 )
            self.counter = 1
        elif self.counter == 1:
            all_pixels = [ (random.randrange(0,255,1),random.randrange(0,255,1),100) ]*360
            self.client.put_pixels( all_pixels )
            self.counter = 0
        else:
            self.counter = 0

client = opc.Client('localhost:7890')
animation = DayTime( client )
while True:
    animation.update()
    time.sleep(0.1)
        
