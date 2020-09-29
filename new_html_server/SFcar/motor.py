import RPi.GPIO as GPIO
import PCA9685
#import time
import logging


# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# ===========================================================================
# Set channel 4 and 5 of the servo driver IC to generate PWM, thus 
# controlling the speed of the car
# ===========================================================================
EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]


class motor(object):
    """Wrapper for the rear drive motors."""
    def __init__(self, pwm, rev_L=False, rev_R=False):
        self.log = logging.getLogger(__name__)
        self.pwm = pwm
        self.rev_0 = rev_L
        self.rev_1 = rev_R

        ## GPIO setup:
        #GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)        # Number GPIOs by its physical location
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode as output
        

    # ========================================================================
    # Adjust the duty cycle of the square waves output from channel 4 and 5 of
    # the servo driver IC, so as to control the speed of the car.
    # ========================================================================
    def setSpeed(self, speed):
        speed *= 40
        self.log.info('motor speed is: %d', speed)
        self.pwm.write(EN_M0, 0, speed)
        self.pwm.write(EN_M1, 0, speed)

    # ========================================================================
    # Control the DC motor to make it rotate clockwise, so the car will 
    # move forward.
    # ========================================================================
    def motor0(self, forward):
        # These are flipped from server/motor.py because we interpret the
        # calibration booleans opposite from the code there.  Hence flip
        # things here to make it go forward if rev_[LR] are False.
        if forward:
            GPIO.output(Motor0_A, GPIO.HIGH)
            GPIO.output(Motor0_B, GPIO.LOW)
        else:
            GPIO.output(Motor0_A, GPIO.LOW)
            GPIO.output(Motor0_B, GPIO.HIGH)

    def motor1(self, forward):
        # See note above on motor0()
        if forward:
            GPIO.output(Motor1_A, GPIO.HIGH)
            GPIO.output(Motor1_B, GPIO.LOW)
        else:
            GPIO.output(Motor1_A, GPIO.LOW)
            GPIO.output(Motor1_B, GPIO.HIGH)

    def forward(self):
        self.motor0(not self.rev_0)
        self.motor1(not self.rev_1)
        self.log.info("motor forward called (%d,%d)", 
                      not self.rev_0, not self.rev_1)

    def backward(self):
        self.motor0(self.rev_0)
        self.motor1(self.rev_1)
        self.log.info("motor backward called (%d,%d)", 
                      self.rev_0, self.rev_1)

    def forwardWithSpeed(self, spd = 50):
        self.setSpeed(spd)
        self.motor0(not self.rev_0)
        self.motor1(not self.rev_1)
        self.log.info("motor forwardWithSpeed(%d) called (%d,%d)",
                      spd, not self.rev_0, not self.rev_1)

    def backwardWithSpeed(self, spd = 50):
        self.setSpeed(spd)
        self.motor0(self.rev_0)
        self.motor1(self.rev_1)
        self.log.info("motor backwardWithSpeed(spd) called (%d,%d)",
                      spd, self.rev_0, self.rev_1)

    def stop(self):
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)


if __name__ == '__main__':
    pwm = PCA9685.PWM()
    m = motor(pwm)
    m.setSpeed(50)
    #m.forward()
    #m.backward()
    m.stop()
