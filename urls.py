from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login', views.login_view),
    url(r'^logout', views.logout_view),
    url(r'^camera', views.camera),
    url(r'^api/set/randomtemperature', views.api_set_randomtemperature),
    url(r'^api/set/ip', views.api_set_ip),
    url(r'^api/get/temperature', views.api_get_temperature),
    url(r'^api/set/temperature', views.api_set_temperature),
    url(r'^api/get/setted_temperature', views.api_get_setted_temperature),
    url(r'^api/set/setted_temperature', views.api_set_setted_temperature),
    url(r'^api/get/door', views.api_get_door),
    url(r'^api/set/door', views.api_set_door),
    url(r'^api/get/light', views.api_get_light),
    url(r'^api/set/light', views.api_set_light),
    url(r'^log', views.showlog),
    url(r'^', views.index),
]
