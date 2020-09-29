import servo
import os
import subprocess

## constants
CHANNEL_PAN = 14
CHANNEL_TILT = 15

class camera(object):
    """Wrapper for the Camera pan/tilt functions."""
    def __init__(self, pwm, calib=None):
        self.pwm = pwm
        self.x_servo = servo.servo(pwm, CHANNEL_PAN, calib.servo_x)
        self.y_servo = servo.servo(pwm, CHANNEL_TILT, calib.servo_y)

    def increase_x(self):
        # these are inverted due to the servo construction
        self.x_servo.decrease()

    def decrease_x(self):
        self.x_servo.increase()

    def increase_y(self):
        self.y_servo.increase()

    def decrease_y(self):
        self.y_servo.decrease()

    def home_x_y(self):
        self.x_servo.home()
        self.y_servo.home()

    def getVal(self):
        return (self.x_servo.getVal(), self.y_servo.getVal())


def mjpg_setup():
    """Run the camera video stream."""
    ## XXX: fix this up to use modern more-portable constructs
    #BASEDIR = "/home/pi/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/mjpg-streamer/mjpg-streamer/"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    BASEDIR = os.path.join(project_root, 'mjpg-streamer', 'mjpg-streamer')
    command = ["./mjpg_streamer", "-i", "./input_uvc.so", 
               "-o", "./output_http.so -w ./www"]
    # since we want to run this in the bg, don't need to keep a handle
    subprocess.Popen(command, cwd=BASEDIR)
