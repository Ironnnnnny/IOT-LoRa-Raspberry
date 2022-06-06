import socket
import time
import sys
import serial
import threading

ser = serial.Serial('/dev/ttyUSB0',9600,timeout = 0.05)
ser_msg = ""
 
HOST_IP = "192.168.12.1"    #我的树莓派作为AP热点的ip地址
HOST_PORT = 7654            #端口号


def connect():
    print("Starting socket: TCP...")
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建socket
    socket_tcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
     
    print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
    host_addr = (HOST_IP, HOST_PORT)
    socket_tcp.bind(host_addr)    #绑定我的树莓派的ip地址和端口号
    socket_tcp.listen(1)	#listen函数的参数是监听客户端的个数，这里只监听一个，即只允许与一个客户端创建连接
    
    while True:
        print ('waiting for connection...')
        socket_con, (client_ip, client_port) = socket_tcp.accept()    #接收客户端的请求
        print("Connection accepted from %s." %client_ip)
     
        socket_con.send("Welcome to RPi TCP server!".encode())    #发送数据
        #t1 = threading.Thread(target = recv_data)
        while True:
            data=socket_con.recv(1024) #接收数据
            ser_data = ser.inWaiting()
            try:
                if ser_data != 0:
                    ser.isOpen()
                    ser_data = ser.readline()
                    ser_msg = ser_data.decode('utf-8')
                    print("ser_data:" + ser_msg)
                    print(0)
                    ser.flushInput()
                    print(1)
                    ser.write(ser_msg.encode())
                    print(2)
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
            if data:    #如果数据不为空，则打印数据，并将数据转发给客户端
                ser.isOpen()
                msg = data.decode('utf-8')
                print(data.decode('utf-8'))
                ser.write(msg.encode())
                                
            elif len(data)==0:
                print("Lost Connection.")
                break
        break
    socket_tcp.close()
    
def recv_data():
    while True:
        ser_data = ser.inWaiting()
        try:
            if ser_data != 0:
                ser_data = ser.readline()
                ser_msg = ser_data.decode()
                print("ser_data:" + ser_msg)
                #socket_con.sendall(ser_msg.encode())
                ser.flushInput()
                
        except UnicodeDecodeError:
            print("UnicodeDecodeError")
            

if __name__ == '__main__' :
    t1 = threading.Thread(target = recv_data)
    t1.start()
    while True:
        connect()