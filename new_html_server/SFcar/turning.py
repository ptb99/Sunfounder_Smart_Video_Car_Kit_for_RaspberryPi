from .servo import servo

## constants
CHANNEL_WHEELS = 0


class turning(object):
    """Wrapper for the Camera pan/tilt functions."""
    def __init__(self, pwm, calib=None):
        self.pwm = pwm
        self.servo = servo(pwm, CHANNEL_WHEELS, calib)

    def left(self):
        self.servo.decrease()

    def right(self):
        self.servo.increase()

    def home(self):
        self.servo.home()
        
    def getVal(self):
        return self.servo.getVal()

    def setVal(self, val):
        return self.servo.setVal(val)
    
