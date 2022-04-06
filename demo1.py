# -*- encoding=utf-8 -*-
import serial
import time
import WriteLog
import socket
import sys


class COM:
	def __init__(self, port, baud):
		self.port = port
		self.baud = int(baud)
		self.open_com = None
		self.get_data_flag = True
		self.real_time_data = ''

  # return real time data form com
	def get_real_time_data(self):
		return self.real_time_data

	def clear_real_time_data(self):
		self.real_time_data = ''

	# set flag to receive data or not
	def set_get_data_flag(self, get_data_flag):
		self.get_data_flag = get_data_flag

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

	def get_data(self, over_time=30):
		all_data = ''
		if self.open_com is None:
			self.open()
		start_time = time.time()
		while True:
			end_time = time.time()
			if end_time - start_time < over_time and self.get_data_flag:
				data = self.open_com.readline(self.open_com.inWaiting())
			# data = self.open_com.read() # read 1 size
				data = str(data)
				if data != '':
					all_data = all_data + data
					print ("ser_msg: " + data)
					self.real_time_data = all_data
					ser.open_com.flushInput()
			else:
				self.set_get_data_flag(True)
				break
		return all_data

def connect():
	HOST_IP = "192.168.12.1"    #我的树莓派作为AP热点的ip地址
	HOST_PORT = 7654            #端口号
	 
	print("Starting socket: TCP...")
	socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建socket
	 
	print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
	host_addr = (HOST_IP, HOST_PORT)
	socket_tcp.bind(host_addr)    #绑定我的树莓派的ip地址和端口号
	socket_tcp.listen(1)	#listen函数的参数是监听客户端的个数，这里只监听一个，即只允许与一个客户端创建连接
	 
	while True:
		print ('waiting for connection...')
		socket_con, (client_ip, client_port) = socket_tcp.accept()    #接收客户端的请求
		com = COM('/dev/ttyUSB0',9600)
		print("Connection accepted from %s." %client_ip)
	 
		socket_con.send("Welcome to RPi TCP server!".encode())    #发送数据
	 
		while True:
			ser_msg = com.get_data
			data=socket_con.recv(1024)    #接收数据
			
			if ser_msg:
				print("socket send 1")
				socket.sendall(ser_msg.encode())
				print("socket send 2")
			
			if data:    #如果数据不为空，则打印数据，并将数据转发给客户端
				print(data.decode('utf-8'))
				socket_con.send(data)
				msg = data.decode('utf-8')
				com.send_data(msg)
	 
	socket_tcp.close()
		

if __name__ == '__main__':
	while True:
		connect()