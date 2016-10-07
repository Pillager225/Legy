#!/usr/bin/python

# TODO: Have the robot give commands in a timely manner, calculate how long it takes to move the servo from its current position to its desired position
# TODO: movement control in a thread
# TODO: accepts input from a socket

from Adafruit_PWM_Servo_Driver import PWM
import time
from Leg import Leg

class MyMovementHandler():
        FL = 0
        FR = 1
        BL = 2
        BR = 3
        
        legs = [Leg([0, 1, 2], FL), Leg([3, 4, 5], FR), Leg([6, 7, 8], BL), Leg([9, 10, 11], BR)]
        ETASet = False
        ETA = .1 # in seconds
        lastTime = 0
        state = -1
        
        gaitCounter = 0
        creepCounter = 0
	turnCounter = 0
	left = True

	def turn(self, direction):
		if direction == "LEFT":
			if self.turnCounter == 0:
				self.legs[self.FR].curlIn()
				self.legs[self.BL].curlIn()	
			elif self.turnCounter == 1:
				self.legs[self.FR].tuck()
				self.legs[self.BL].tuck()
			elif self.turnCounter == 2:
				self.legs[self.FR].stand()
				self.legs[self.BL].stand()
			self.ETA = self.legs[self.BR].ETA
			if self.ETA < self.legs[self.BL].ETA:
				self.ETA = self.legs[self.BL].ETA
			if self.ETA < self.legs[self.FR].ETA:
				self.ETA = self.legs[self.FR].ETA
			if self.ETA < self.legs[self.FL].ETA:
				self.ETA = self.legs[self.FL].ETA
		self.turnCounter += 1
		if self.turnCounter > 2:
			self.turnCounter = 0

        def gait(self, direction):
		print self.gaitCounter
                if self.gaitCounter == 0:
			if self.left:
				self.legs[self.FL].raiseLeg()
				self.legs[self.FL].pushOut()
			else:
				self.legs[self.FR].raiseLeg()
				self.legs[self.FR].pushOut()
			self.legs[self.BR].raiseLeg()
			self.legs[self.BL].raiseLeg()
                elif self.gaitCounter == 1:
			self.legs[self.BR].pullIn()
			self.legs[self.BL].pullIn()
                elif self.gaitCounter == 2:
			if self.left:
				self.legs[self.FL].lowerLeg()
				self.legs[self.FL].pullInFront()
				self.legs[self.FR].lowerLeg()
			else:
				self.legs[self.FR].lowerLeg()
				self.legs[self.FR].pullInFront()
				self.legs[self.FL].lowerLeg()
			self.legs[self.BR].tallStand90Hip()
			self.legs[self.BL].tallStand90Hip()
			self.left = not self.left
		self.ETA = self.legs[self.BR].ETA
		if self.ETA < self.legs[self.BL].ETA:
			self.ETA = self.legs[self.BL].ETA
		if self.ETA < self.legs[self.FR].ETA:
			self.ETA = self.legs[self.FR].ETA
		if self.ETA < self.legs[self.FL].ETA:
			self.ETA = self.legs[self.FL].ETA
        	if(direction == "FORWARD"):
        		self.gaitCounter += 1
        	elif(direction == "BACKWARD"):
        		self.gaitCounter -= 1
                if self.gaitCounter > 2:
                	self.gaitCounter = 0
        	elif self.gaitCounter < 0:
        		self.gaitCounter = 2
        
        def creep(self, direction):
		print self.creepCounter
		self.ETA = self.legs[self.BR].ETA
		if self.creepCounter == 0:
			self.legs[self.BR].raiseLeg()
		if self.ETA < self.legs[self.BL].ETA:
			self.ETA = self.legs[self.BL].ETA
		if self.ETA < self.legs[self.FR].ETA:
			self.ETA = self.legs[self.FR].ETA
		if self.ETA < self.legs[self.FL].ETA:
			self.ETA = self.legs[self.FL].ETA
        	if(direction == "FORWARD"):
        		self.creepCounter += 1
        	elif(direction == "BACKWARD"):
        		self.creepCounter -= 1
		if self.creepCounter >= 16:
			self.creepCounter = 0
		elif self.creepCounter <= -1:
			self.creepCounter = 15
        
	def stand(self):
		self.legs[self.FL].stand()
		self.legs[self.FR].stand()
		self.legs[self.BL].stand()
		self.legs[self.BR].stand()
		self.ETA = self.legs[self.FL].ETA
		if self.ETA < self.legs[self.FR].ETA:
			self.ETA = self.legs[self.FR].ETA
		if self.ETA < self.legs[self.BL].ETA:
			self.ETA = self.legs[self.BL].ETA
		if self.ETA < self.legs[self.BR].ETA:
			self.ETA = self.legs[self.BR].ETA
        
        def handleMovement(self):
		i = 0
		self.stand()
        	while True:
        		currentTime = time.clock()
			if currentTime-self.lastTime >= self.ETA:
			#	print self.state
			#	s = "hit enter for next command"
	                #	i = raw_input(s)
        			if "GAIT" in self.state:
        				if "FORWARD" in self.state:
        					self.gait("FORWARD")
        				elif "BACKWARD" in self.state:
        					self.gait("BACKWARD")
				elif "CREEP" in self.state:
					if "FORWARD" in self.state:
						self.creep("FORWARD")
					elif "BACKWARD" in self.state:
						self.creep("BACKWARD")
				elif "STAND" in self.state:
					self.stand()
				elif "LEAP" in self.state:
					if "FORWARD" in self.state:
						self.leap("FORWARD")
					elif "BACKWARD" in self.state:
						self.leap("BACKWARD")
				elif "TURN" in self.state:
					if "LEFT" in self.state:
						self.turn("LEFT")
					else:
						self.turn("RIGHT")
        			self.lastTime = currentTime
        
