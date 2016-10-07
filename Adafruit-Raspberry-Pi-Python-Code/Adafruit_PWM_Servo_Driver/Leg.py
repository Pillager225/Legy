#!/usr/bin/env python

from Adafruit_PWM_Servo_Driver import PWM
from Joint import Joint
import time

# FL
#	KNEE	servoMin = 170, servoMax = 650, 90 = 400	
# 	FOOT	servoMin = 170, servoMax = 645, 90 = 400
# FR
#	KNEE	servoMin = 170, servoMax = 630, 90 = 400
#	FOOT	servoMin = 170, servoMax = 640, 90 = 400
# BL
#	KNEE	servoMin = 170, servoMax = 645

class Leg:
	FL = 0
	FR = 1
	BL = 2
	BR = 3

	HIP = 0
	KNEE = 1
	FOOT = 2

	state = -1
	hip = None
	knee = None
	foot = None
	pwm = PWM(0x40)
	leg = None

	# in seconds
	ETA = 1
	
	def __init__(self, chs, leg):
		self.leg = leg
		if leg == self.FL:
			self.hip = Joint(chs[0], "FLHIP")
			self.knee = Joint(chs[1], "FLKNEE")
			self.foot = Joint(chs[2], "FLFOOT")
		elif leg == self.FR:
			self.hip = Joint(chs[0], "FRHIP")
			self.knee = Joint(chs[1], "FRKNEE")
			self.foot = Joint(chs[2], "FRFOOT")
		elif leg == self.BR:
			self.hip = Joint(chs[0], "BRHIP")
			self.knee = Joint(chs[1], "BRKNEE")
			self.foot = Joint(chs[2], "BRFOOT")
		elif leg == self.BL:
			self.hip = Joint(chs[0], "BLHIP")
			self.knee = Joint(chs[1], "BLKNEE")
			self.foot = Joint(chs[2], "BLFOOT")
		self.state = "initialized"

	
	def raiseLeg(self):
#		if self.leg == self.FL or self.leg == self.BR:
		self.hip.moveToAngle(90)
#		elif self.leg == self.FR or self.leg == self.BL:
#			self.hip.moveToAngle(60)
		self.ETA = self.hip.ETA
		self.state = "RAISED"

	def lowerLeg(self):
#		if self.leg == self.FL or self.leg == self.BR:
		self.hip.moveToAngle(70)
#		else:
#			self.hip.moveToAngle(120)
		self.ETA = self.hip.ETA
		self.state = "LOWERED"

	def forwardStep(self):
		if self.leg == self.FL or self.leg == self.FR:
			self.knee.moveToAngle(70)
			self.foot.moveToAngle(70)
		else:
			self.knee.moveToAngle(140)
			self.foot.moveToAngle(110)
		self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		if("RAISED" in self.state):
			self.state = "RAISED_FORWARD"
		elif("LOWERED" in self.state):
			self.state = "LOWERED_FORWARD"
		else:
			self.state = "FORWARD"
	
	def backwardStep(self):
		if self.leg == self.FL or self.leg == self.FR:
			self.knee.moveToAngle(140)
			self.foot.moveToAngle(110)
		elif self.leg == self.BR or self.leg == self.BL:
			self.knee.moveToAngle(70)
			self.foot.moveToAngle(70)
		self.ETA = self.knee.ETA
		if self.ETA < self.knee.ETA:
			self.ETA = self.knee.ETA
		if("RAISED" in self.state):
			self.state = "RAISED_BACKWARD"
		elif("LOWERED" in self.state):
			self.state = "LOWERED_BACKWARD"
		else:
			self.state = "BACKWARD"

	def tallStand(self):
		self.hip.moveToAngle(70)
		self.knee.moveToAngle(130) #130
		self.foot.moveToAngle(55) #55
		self.ETA = self.hip.ETA
		if self.ETA < self.knee.ETA:
			self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		self.state = "TALL_STAND"

	def stand(self):
		self.hip.moveToAngle(70)
		self.knee.moveToAngle(90) #130
		self.foot.moveToAngle(90) #55
		self.ETA = self.hip.ETA
		if self.ETA < self.knee.ETA:
			self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		self.state = "STAND"

	def dip(self): 
		if self.leg == self.FL or self.leg == self.FR:
			self.knee.moveToAngle(135)
			self.foot.moveToAngle(70)
		else:
			self.knee.moveToAngle(135)
			self.foot.moveToAngle(70)
		self.ETA = self.hip.ETA
		self.state = "DIP"
	
	def undip(self):
		self.stand()

	def cornerDip(self):
		if self.leg == self.FL or self.leg == self.FR:
			self.hip.moveToAngle(100)
			self.knee.moveToAngle(120)
			self.foot.moveToAngle(70)
		else:
			self.hip.moveToAngle(100)
			self.knee.moveToAngle(120)
			self.foot.moveToAngle(70)
		self.ETA = self.hip.ETA
		self.state = "CORNER_DIP"

	def pullIn(self):
		if self.leg == self.FL or self.leg == self.BR:
			self.knee.moveToAngle(175)
			self.foot.moveToAngle(15)
		else:
			self.knee.moveToAngle(175)
			self.foot.moveToAngle(15)
		self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		self.state = "PULLED_IN"

	def pushOut(self):
		if self.leg == self.FR or self.leg == self.BL:
			self.knee.moveToAngle(70)
			self.foot.moveToAngle(90)
		else:
			self.knee.moveToAngle(70)
			self.foot.moveToAngle(90)
		self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		self.state = "PUSHED_OUT"

	def tallStand90Hip(self):
		self.hip.moveToAngle(90)
		self.knee.moveToAngle(130) #130
		self.foot.moveToAngle(55) #55
		self.ETA = self.hip.ETA
		if self.ETA < self.knee.ETA:
			self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		self.state = "TALL_STAND"
	
	def pullInFront(self):
		if self.leg == self.FL or self.leg == self.BR:
			self.knee.moveToAngle(160)
			self.foot.moveToAngle(60)
		else:
			self.knee.moveToAngle(160)
			self.foot.moveToAngle(60)
		self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		self.state = "PULLED_IN"

	def curlIn(self):
		if self.leg == self.FL or self.leg == self.BR:
			self.knee.moveToAngle(160)
			self.foot.moveToAngle(110)
		else:
			self.knee.moveToAngle(160)
			self.foot.moveToAngle(110)
		self.ETA = self.knee.ETA
		if self.ETA < self.foot.ETA:
			self.ETA = self.foot.ETA
		self.state = "CURLED_IN"	

	def tuck(self):
		self.hip.moveToAngle(40)
		self.DTA = self.hip.ETA
		self.state = "tucked"
