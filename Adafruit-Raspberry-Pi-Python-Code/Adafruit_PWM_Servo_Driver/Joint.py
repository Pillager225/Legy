#!/usr/bin/env python

from Adafruit_PWM_Servo_Driver import PWM

class Joint:
	channel = 0
	pwm = PWM(0x40)
	servoMin = 0
	servoMax = 0
	servoSpeed = .00333333333333333 # .2/60 sec/deg | .2/60 at 4v, .16/60 at 6v Tower Pro MG995 
	curAngle = 90 
	leg = 0

	ETA = 1
	ETASet = False

	def __init__(self, channel, joint):
		self.channel = channel
		self.leg = joint[0:2]
		if joint  == "FLHIP":
			self.servoMin = 165
			self.servoMax = 600
		elif joint == "FLKNEE":
			self.servoMin = 145
			self.servoMax = 650
		elif joint == "FLFOOT":
			self.servoMin = 170
			self.servoMax = 645
		elif joint == "FRHIP":
			self.servoMax = 640
			self.servoMin = 175
		elif joint == "FRKNEE":
			self.servoMax = 630
			self.servoMin = 170
		elif joint == "FRFOOT":
			self.servoMax = 640
			self.servoMin = 170
		elif joint == "BRHIP":
			self.servoMin = 170
			self.servoMax = 650
		elif joint == "BRKNEE":
			self.servoMin = 170
			self.servoMax = 645
		elif joint == "BRFOOT":
			self.servoMin = 160
			self.servoMax = 650
		elif joint == "BLHIP":
			self.servoMax = 650 #635
			self.servoMin = 170 #180
		elif joint == "BLKNEE":
			self.servoMax = 650
			self.servoMin = 170
		elif joint == "BLFOOT":
			self.servoMax = 650
			self.servoMin = 150
		self.moveToAngle(self.curAngle)
		
	def reMap(self, val, startLow, startHigh, endLow, endHigh):
		return int(round((val-startLow)*(endHigh-endLow)/(startHigh-startLow)+endLow))

	# angle from 0-180
	def moveToAngle(self, angle):
	#         	 s = "hit enter for next command"
	#                i = raw_input(s)
		tmpInt = self.servoSpeed*abs(angle-self.curAngle)
		if self.ETASet == False or self.ETA < tmpInt:
                        self.ETA = tmpInt
		if self.leg == "FR" or self.leg == "BL":
               		pulse = self.reMap(angle, 180, 0, self.servoMin, self.servoMax)
		else:
               		pulse = self.reMap(angle, 0, 180, self.servoMin, self.servoMax)
                if(pulse > self.servoMax):
                        pulse = self.servoMax
                if(pulse < self.servoMin):
                        pulse = self.servoMin
                self.curAngle = angle
                self.pwm.setPWM(self.channel, 0, pulse)

