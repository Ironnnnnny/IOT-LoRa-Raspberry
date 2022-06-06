# -*- encoding=utf-8 -*-
import serial
import time
import socket
import sys
from threading import Thread


class COM:
	def __init__(self, port, baud):
		self.port = port
		self.baud = int(baud)
		self.open_com = serial.Serial(self.port, self.baud,timeout = 0.05)

	def open(self):
		self.open_com = serial.Serial(self.port, self.baud,timeout = 0.05)


	def close(self):
		if self.open_com is not None and self.open_com.isOpen:
			self.open_com.close()

	def send_data(self, data):
		if self.open_com is None:
			self.open()
		success_bytes = self.open_com.write(data.encode('UTF-8'))
		return success_bytes

	def get_data(self):
		data = self.open_com.inWaiting()
		try:
			if data != 0:
				data = self.open_com.readline()
				data = data.decode('utf-8')
				self.open_com.flushInput()
				return data
		except UnicodeDecodeError:
			print("UnicodeDecodeError")

def connect():
	HOST_IP = "192.168.12.1"    #我的树莓派作为AP热点的ip地址
	HOST_PORT = 7654            #端口号
	 
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
		com = COM('/dev/ttyUSB0',9600)
		print("Connection accepted from %s." %client_ip)
	 
		socket_con.sendall("Welcome to RPi TCP server!".encode())    #发送数据
		count = 0
		
		def c_recv():
			while True:
				ser_data = com.get_data()
				if ser_data:
					print("socket send 1")
					socket_con.sendall(ser_data.encode())
					print("ser_msg: " + str(ser_data))
					print("socket send 2")
				
		t1 = Thread(target=c_recv)
		t1.start()
		
		while True:
			data = socket_con.recv(1024)    #接收数据
			'''ser_data = com.get_data()
			print("ser_msg: " + str(ser_data))
			if ser_data:
				print("socket send 1")
				socket_con.sendall(ser_data.encode())
				print("socket send 2")'''
				
			if data:    #如果数据不为空，则打印数据
				#socket_con.senda(data)
				count += 1
				msg = data.decode('utf-8')
				print ("msg: " + msg)
				com.send_data(msg)
				print ("count: %d" %count)
			
			elif len(data)==0:
				print("Lost Connection.")
				break
		break
	com.close()
	socket_tcp.close()
		

if __name__ == '__main__':
	while True:
		connect()