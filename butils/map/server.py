import socket
import sys
import threading
import signal
import yaml
from mapserver import MapServer

NUM_SLOT_MAX = 1000
CONFIG_FILE = "config.yml"
properties = None

with open(CONFIG_FILE,'r') as f:
	properties = yaml.load(f)


map_server = MapServer(NUM_SLOT_MAX,properties)
map_server.register()

IP   = properties['server']['ip']
PORT = properties['server']['port']

class ClientThread(threading.Thread):

	def __init__(self,con,ip,port,map_server):
		print "Start constructor client thread"
		threading.Thread.__init__(self)
		self.con = con
		self.ip = ip
		self.port = port
		self.map_server=map_server
		print "End constructor client thread"

	def run(self):
		try:
			while(True):
				print "Waiting for data"
				data = self.con.recv(4096)
				if data:
					self.map_server.processMessage(data,self.con)
				else:
					self.con.close()
					return
		except Exception as ex:
			print ex
			self.con.close()

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s_address = (IP,PORT)
sock.bind(s_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Enable reuse of the port

sock.listen(10)

def exit_handler(signa,frame):
	print "Exiting program, closing socket"
	sys.exit("Control-C called")
	sock.close()
	map_server.stop()

signal.signal(signal.SIGINT,exit_handler)

threads = []

while(True):
	try:
		print "waiting for connection"
		(con, (ip,port)) = sock.accept()
		print "Connection accepted, starting client thread"
		t = ClientThread(con,ip,port,map_server)
		t.start()
		threads.append(t)
	except Exception as e:
		print "Error outer loop: ",e

for t in threads:
    t.join()

print "Closing the server"
sock.close();
