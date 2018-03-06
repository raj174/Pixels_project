from threading import Timer
import time


def printit():
  print "Hello, World!"

j = Timer(5, printit)
j.start()
for i in range(10000):
    print i
    
