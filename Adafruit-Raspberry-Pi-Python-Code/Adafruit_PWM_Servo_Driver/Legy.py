#!/usr/bin/env python
import thread
import time
import SocketServer
from MovementController import MovementController
from WifiServer import WifiServer

class Starter:
	movementController = None
	controlServer = None
	mPipe = None
	cPipe = None

	def __init__(self):
		self.makeClasses()
		self.startProcesses()
		# Catch SIGINT from ctrl-c when run interactively.
		signal.signal(signal.SIGINT, self.signal_handler)
		# Catch SIGTERM from kill when running as a daemon.
		signal.signal(signal.SIGTERM, self.signal_handler)
		# This thread of execution will sit here until a signal is caught
		signal.pause()

	def makeClasses(self):
		manager = Manager()
		self.mPipe, pipeM = Pipe()
		self.cPipe, pipeC = Pipe()
		controlQueue = manager.Queue()
		self.movementController = MovementController(controlQueue=controlQueue, pipe=pipeM)
		self.movmentController.state = "STAND"
		self.controlServer = WifiServer(queue=controllerQueue, pipe=pipeC)

	def startProcesses(self):
		self.movementController.start()
		self.controlServer.start() 

	def signal_handler(self, signal, frame):
		self.exitGracefully()

	def exitGracefully(self):
		try:
			print "Program was asked to terminate."
			if self.movementController:
				self.mPipe.send('stop')	
			if self.controlServer:
				self.cPipe.send('stop')
			sys.stdout.write("Waiting for threads to exit...")
			sys.stdout.flush()
			self.movementController.join()
			self.controlServer.join()
			print "Done"
			sys.exit(0)
		except Exception as msg:
			print "An exception occured while trying to terminate"
			print msg
			sys.exit(1)

if __name__ == "__main__":
	s = Starter()
