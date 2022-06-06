import serial
import time
import threading

ser = serial.Serial('/dev/ttyUSB0',9600,timeout = 0.05)
i = 0

def recv_data():
    while True:
        data = ser.inWaiting()
        try:
            if data != 0:
                data = ser.readline()
                print("receive:  " + data.decode())
                ser.flushInput()
        except UnicodeDecodeError:
            print("UnicodeDecodeError")

t1 = threading.Thread(target = recv_data)
if __name__ == '__main__':
    t1.start()
    while True:
        ser.isOpen()
        ser.write(str(i).encode())
        print(i)
        i = i + 1 
        time.sleep(2)
        
