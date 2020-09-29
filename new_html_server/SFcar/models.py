from django.db import models

# Create your models here.

### my measurements of car calibration
# chan  0 = turn wheels - 350 to 430 to 510
# chan 14 = camera pan  - 220 to 410 to 640
# chan 15 = camera tilt - 260 to 320 to 550

class ServoCalib(models.Model):
    name = models.CharField(max_length=128)
    minVal = models.SmallIntegerField(default=200)
    maxVal = models.SmallIntegerField(default=700)
    defVal = models.SmallIntegerField(default=450)

    def __str__(self):
        return "Servo - " + self.name


class Calibration(models.Model):
    servo_x = models.ForeignKey(ServoCalib, 
                                on_delete=models.CASCADE, related_name='x')
    servo_y = models.ForeignKey(ServoCalib, 
                                on_delete=models.CASCADE, related_name='y')
    servo_turn = models.ForeignKey(ServoCalib, 
                                   on_delete=models.CASCADE, 
                                   related_name='turn')
    forward0 = models.BooleanField(default=False)
    forward1 = models.BooleanField(default=False)
    completed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "calibration completed " + str(self.completed)


def getLatestConfig():
    """Helper function to extract the current config."""
    calib = Calibration.objects.order_by('-completed')
    if len(calib) > 0:
        return calib[0]
    else:
        return Calibration()
