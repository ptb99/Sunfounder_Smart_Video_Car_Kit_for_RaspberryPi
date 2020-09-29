from django.contrib import admin

# Register your models here.
from .models import ServoCalib, Calibration

admin.site.register(ServoCalib)
admin.site.register(Calibration)
