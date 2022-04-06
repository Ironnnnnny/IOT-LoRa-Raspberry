import serial
import time
ser = serial.Serial('/dev/ttyUSB0',9600,timeout = 0.05)
i = 0
while True:
    ser.isOpen()
    ser.write(str(i).encode())
    print(i)
    i = i + 1 
    time.sleep(0.5)
