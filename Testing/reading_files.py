

file = open("newfile.txt", "r")
j = file.read( ).split(':')
sunrise_sec = j[0]
sunset_sec = j[1]

print sunrise_sec,sunset_sec


file.close()
