#!/usr/bin/env python
import thread
import time
import SocketServer
from MyMovementHandler import MyMovementHandler

def startLegy():
	try:
		movement = MyMovementHandler()
		movement.state = "STAND" 
		movement.handleMovement()
#self.movement.state = "CREEP_FORWARD"
	except Exception as msg:
		print msg
#self.movement.state = "GAIT_FORWARD"
#self.movement.state = "LEAP_FORWARD"
# copied from https://docs.python.org/2/library/socketserver.html
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    movement = None


    def startLegy(self):
        self.movement = MyMovementHandler()
        thread.start_new_thread(self.movement.handleMovement, ())
        #self.movement.state = "CREEP_FORWARD"
        self.movement.state = "STAND" 
        #self.movement.state = "GAIT_FORWARD"
        #self.movement.state = "LEAP_FORWARD"

    def handle(self):
	self.startLegy()
	while True:
        	# self.request is the TCP socket connected to the client
        	self.data = self.request.recv(2).strip()
		if len(self.data) > 0:
			bytes = bytearray(self.data)
			for b in bytes:
				print int(bin(b), 2)
			if len(bytes) == 10000:
				tempState = "STOP"
				# if int(bin(bytes[1])) == 1000 0000
				if int(bin(bytes[1]), 2)>>7&1 == 1: #are we connected
					b0 = int(bin(bytes[0]), 2)
					print b0
#					if(b0>>2&1 == 1): # verticle
					#	if(b0>>3&1 == 1):
#							tempState = "GAIT_FORWARD"
						#else:
							#tempState = "GAIT_BACKWARD"
					#if(b0&1 == 1): # horizontal
						#if(b0>>1&1 == 1):
						#	tempState = "TURN_LEFT"
					#else:
					#	tempState = "STOP"
				else: 
					tempState = "STOP"
				self.movement.state = tempState
						
	        	# just send back the same data, but upper-cased
	        	self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "", 12345
    startLegy()
    # Create the server, binding to localhost on port 12345
#    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
 #   server.serve_forever()
