# SFcar/urls.py - routing file SFcar views

from django.conf.urls import url, include
from django.views.generic import TemplateView
from SFcar import views


calibratepatterns = [
    url(r'^(getconfig)', views.CalibrationView.as_view()),
    url(r'^(turning)/(.)/(\d{1,3})', views.CalibrationView.as_view()),
    url(r'^(motor)/(run)', views.CalibrationView.as_view()),
    url(r'^(motor)/(stop)', views.CalibrationView.as_view()),
    url(r'^(motor)/(left)/(reverse)', views.CalibrationView.as_view()),
    url(r'^(motor)/(right)/(reverse)', views.CalibrationView.as_view()),
    url(r'^(pan)/(.)/(\d{1,3})', views.CalibrationView.as_view()),
    url(r'^(til[et])/(.)/(\d{1,3})', views.CalibrationView.as_view()),
    url(r'^(confirm)', views.CalibrationView.as_view()),
]


urlpatterns = [
    # main user-visible pages
    url(r'^$', views.index_redirect),
    url(r'^test/(.)/(\d{0,3})', views.test, name='test'),
    url(r'^client/', TemplateView.as_view(template_name='SFcar/client.html'), 
        name='client'),
    #url(r'^calibration/', TemplateView.as_view(template_name='SFcar/calibrate.html'),  name='calibration'),

    # run-mode REST API
    url(r'^runmode', views.run_mode, name='runmode'),
    url(r'^motor/(?P<direction>\w+)', 
        views.MotorView.as_view(), name='motor'),
    url(r'^motor/set/speed/(?P<speed>\d{1,3})', 
        views.MotorView.as_view(), name='motorspeed'),
    url(r'^camera/(?P<dir>\w+)/(?P<axis>\w+)', 
        views.CameraView.as_view(), name='camera'),
    url(r'^camera/(?P<dir>\w+)', 
        views.CameraView.as_view(), name='camerahome'),
    url(r'^turning/(?P<angle>\d{1,3})', views.turning, name='turning'),
    #url(r'^turning/(?P<dir>left)', views.turning, name='turning'),
    #url(r'^turning/(?P<dir>right)', views.turning, name='turning'),


    # calibration-mode REST API
    url(r'^calibrationmode', views.calibration_mode, name='calibrationmode'),
    url(r'^calibrate/', include(calibratepatterns)),
]
