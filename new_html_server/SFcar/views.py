from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .car import car
#import camera
#import turning
#import motor
from .models import Calibration, getLatestConfig

# Create your views here.

the_car = None

def getCar():
    """Return singleton handle to car object.  Init if needed."""
    global the_car
    if not the_car:
        calib = getLatestConfig()
        the_car = car(calib)
    return the_car


class MotorView(View):
    def get(self, request, *args, **kwargs):
        retval = "Err"
        if 'speed' in kwargs:
            retval = self.set_speed(kwargs['speed'])
        else:
            drive = getCar().drive
            if 'direction' in kwargs:
                dir = kwargs['direction']
                if dir == 'forward':
                    drive.forward()
                    retval = 'Motor forward'
                elif dir == 'backward':
                    drive.backward()
                    retval = 'Motor backward'
                elif dir == 'stop':
                    drive.stop()
                    retval = 'Motor stop'
            else:
                retval = 'Unknown /motor/ args ' + ' '.join(args)
                # should we return an error page?
        return HttpResponse(retval)

    def set_speed(request, speed):
        speed = int(speed)
        if speed < 24:
                speed = 24
        if speed > 100:
                speed = 100
        getCar().drive.setSpeed(speed)
        text = "Speed set to " + speed
        return text


def turning(request, angle):
    getCar().turn.setVal(angle)
    text = "Turning angle" + angle
    return HttpResponse(text)


class CameraView(View):
    def get(self, request, *args, **kwargs):
        retval = "Error"
        camera = getCar().cam
        if kwargs['dir'] == 'home':
            camera.home_x_y()
            retval = 'Camera back to defaultrequest'
        elif kwargs['axis'] == 'x':
            if kwargs['dir'] == 'increase':
                camera.increase_x()
                retval = 'Camera x+'
            elif kwargs['dir'] == 'decrease':
                camera.decrease_x()
                retval = 'Camera x-'
        elif kwargs['axis'] == 'y':
            if kwargs['dir'] == 'increase':
                camera.increase_y()
                retval = 'Camera y+'
            elif kwargs['dir'] == 'decrease':
                camera.decrease_y()
                retval = 'Camera y-'
        return HttpResponse(retval)
            

class CalibrationView(View):
    def get(self, request, *args):
        calib = getLatestConfig()
        car = getCar()
        retval = 'Error'
        if args[0] == 'getconfig':
            retval = "%s\n%s\n%s" % (calib.servo_turn.defVal, 
                                     calib.servo_x.defVal,
                                     calib.servo_y.defVal)
        elif args[0] == 'turning':
            offset = int(args[2])
            if args[1] == '-':
                offset *= -1 
            #car_dir.calibrate(offset)
            retval = 'offset: ' + str(offset)
        elif args[0] == 'motor':
            if args[1] == 'run':
                car.drive.setSpeed(50)
                car.drive.forward()
                retval = 'Motors Runing'
            elif args[1] == 'stop':
                car.drive.stop()
                retval = 'Motors stop'
            elif args[1] == 'left' and args[2] == 'reverse':
                calib.forward0 = not calib.forward0
                calib.save()
                car.drive.motor0(not calib.forward0)
                retval = 'left motor reverse to ' + str(calib.forward0)
            elif args[1] == 'right' and args[2] == 'reverse':
                calib.forward1 = not calib.forward1
                calib.save()
                car.drive.motor1(not calib.forward1)
                retval = 'right motor reverse to ' + str(calib.forward1)
            else:
                pass
                # return error
        elif args[0] == 'pan':
            offset = int(args[2])
            if args[1] == '-':
                offset *= -1 
            #car.cam.calibrate(offset_x, offset_y)
            retval = 'Pan offset set to: ' + str(offset)
        elif args[0] == 'tile' or args[0] == 'tilt':
            offset = int(args[2])
            if args[1] == '-':
                offset *= -1 
            #car.cam.calibrate(offset_x, offset_y)
            retval = 'Tile offset set to: ' + str(offset)
        elif args[0] == 'confirm':
            # calib.save()
            retval = 'Saved new calib'
        else:
            pass
            # return error
        return HttpResponse(retval)


def run_mode(request):
    getCar().cam.home_x_y()
    return HttpResponse("Run mode start")

def calibration_mode(request):
    car = getCar()
    car.cam.home_x_y()
    car.turn.home()
#     video_dir.calibrate(offset_x, offset_y)
#     car_dir.calibrate(offset)
    return HttpResponse("Calibration mode start")

def test(request, direction, text):
    """Dummy function to test the API??"""
    text = direction + str(text)
    return HttpResponse(text)

def index_redirect(request):
    return redirect('/client')
