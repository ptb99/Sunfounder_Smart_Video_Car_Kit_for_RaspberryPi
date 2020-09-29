#! /usr/bin/python

#import PCA9685
#import calibration

import logging


class servo(object):
    """One instance of a PWM-controlled servo motor in the robot car."""
    def __init__(self, pwm, channel, calib=None):
        self.log = logging.getLogger(__name__)
        self.pwm = pwm
        self.chan = channel
        if calib:
            self.minVal = calib.minVal
            self.maxVal = calib.maxVal
            self.defVal = calib.defVal
        else:
            self.minVal = 200
            self.maxVal = 700
            self.defVal = 450
        self.currentVal = self.defVal

    def increase(self, step=25):
        self.currentVal += step
        if self.currentVal > self.maxVal:
            self.currentVal = self.maxVal
        logging.info("Chan %d increase to %d", self.chan, self.currentVal)
        self.pwm.write(self.chan, 0, self.currentVal)

    def decrease(self, step=25):
        self.currentVal -= step
        if self.currentVal < self.minVal:
            self.currentVal = self.minVal
        logging.info("Chan %d decrease to %d", self.chan, self.currentVal)
        self.pwm.write(self.chan, 0, self.currentVal)

    def home(self):
        self.currentVal = self.defVal
        logging.info("Chan %d home to %d", self.chan, self.currentVal)
        self.pwm.write(self.chan, 0, self.currentVal)

    def getVal(self):
        return self.currentVal

    def setVal(self, angle):
        """Map from angle in a range of 0-255 to our calibration range."""
        val = int(angle) / 255.0 * (self.maxVal - self.minVal) + self.minVal
        self.currentVal = int(val)
        logging.info("Chan %d set to %d", self.chan, self.currentVal)
        self.pwm.write(self.chan, 0, self.currentVal)
        
