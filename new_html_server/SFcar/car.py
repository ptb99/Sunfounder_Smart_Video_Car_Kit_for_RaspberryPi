from .PCA9685 import PWM
from .camera import camera, mjpg_setup
from .turning import turning
from .motor import motor
from .models import Calibration


class car(object):
    """Wrapper for all the state involved in the SunFounder robot car."""

    def __init__(self, calib=None):
        # handle to the Pulse-Width Modulation chip used for controls
        self.pwm = PWM()
        if not calib:
            # if no calibration passed in, use defaults
            calib = Calibration()

        # init the 3 elements
        self.cam = camera(self.pwm, calib)
        self.turn = turning(self.pwm, calib.servo_turn)
        self.drive = motor(self.pwm, calib.forward0, calib.forward1)

        # spawn the mjpg feed
        mjpg_setup()

        # move servos to default
        self.cam.home_x_y()
        self.turn.home()
        self.drive.setSpeed(50)

    #def something-about-calibration
