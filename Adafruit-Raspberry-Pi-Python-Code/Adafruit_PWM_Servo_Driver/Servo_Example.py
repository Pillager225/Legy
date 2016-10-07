#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)
channel = 6
increment = -5
servoMin = 170  # Min pulse length out of 4096 (1ms for 60Hz)
servoMax = 645  # Max pulse length out of 4096 (2.5ms for 60Hz)

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

# angle from 0-180
def moveTo(channel, angle):
  pulse = angle*(servoMax-servoMin)/180+servoMin
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
#  pwm.setPWM(0, 0, servoMin)
#  print "min"
#  time.sleep(1)
#  pwm.setPWM(0, 0, servoMax)
#  print "max"
#  time.sleep(1)
  pulse = 400
  pwm.setPWM(channel, 9, pulse)
  while True:
    s = "Pulse is at " + str(pulse) + "hit enter to decrease by 5"
    i = raw_input(s)
    pulse += increment
    pwm.setPWM(channel, 0, pulse)
