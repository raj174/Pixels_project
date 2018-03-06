This folder contains files that are ment for the pixel project.

The main file to run is Master.py for animations.
Before opening Master.py and connecting to fadecandy, run Sunrise_Sunset_API.py to get the latest values from the internet.
The opc.py is the library needed for program to run on the led strip or simulator.
All the libraries used in Master.py can be found in the Libraries Folder.
Some of the libraries might need to be installed.
The animations I am currently working on or had worked on are in the Trying Folder.
The Arduino folder has the arduino sketch I am using in the arduino,it also has a read_serial.py file which was used for testing but can also be used to play with the lights.

The Master.py reads the the text file that gives Sunrise and Sunset time if its not connected to the internet.
It also checks if the Arduino is available for serial communication, the falling function uses the arduino.
Every five minutes it compares sunrise and sunset with the current time.
Depending on this it plays the set of animations. 
If the fadecandy is not connected to the internet you'd need to run the Sunrise_Sunset_API.py every morning so it can get the new values.

The current location for Sunset and Sunrise is near the Ritterman Building, Middlesex University

Some of the Arduino code and Python Code have been taken from example codes that were provided by the libraries used.
