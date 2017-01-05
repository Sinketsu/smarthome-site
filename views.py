from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Log, Thing, Record 
from . import dbwork
from . import logging
import socket
import json
import random
import datetime
import requests

def index(request):
	if request.user.is_authenticated():
		door_bool = True if dbwork.get_last_record(rec_type = 'DOOR').value == '1' else False
		light_bool = True if dbwork.get_last_record(rec_type = 'LIGHT').value == '1' else False
		return render_to_response('index.html', {'temperature' : dbwork.get_last_record(rec_type = 'TEMPERATURE').value,
							'setted_temperature' : dbwork.get_last_record(rec_type = 'SETTED_TEMPERATURE').value,
							'door_label' : 'открыта' if door_bool else 'закрыта',
							'door_open' : 'checked' if door_bool else '',
							'light_label' : 'включен' if light_bool else 'выключен',
							'light_on' : 'checked' if light_bool else '',
							})
	else:
		return redirect('/login')

def camera(request):
	if request.user.is_authenticated():
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("gmail.com", 80))
		return render_to_response('camera.html', {'ip' : s.getsockname()[0],
							})
	else: 
		return redirect('/login')

def login_view(request):
	if request.method == 'GET':
		return render_to_response('login.html', {})
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/') 
		else:
			return HttpResponse('Login or password is invalid') #переделать

def logout_view(request):
	logout(request)
	return redirect('/login')

def api_get_temperature(request):
	logging.add(request, "GET TEMPERATURE")
	item = dbwork.get_last_record(rec_type = 'TEMPERATURE')
	return HttpResponse(item.value)


def api_set_temperature(request):
	logging.add(request, "SET TEMPERATURE")
	if request.method == 'POST':
		data = request.POST['data']
	else:
		data = request.GET['data']
	param_list = json.loads(data)
	value = param_list['value']
	dbwork.add_record(rec_type = 'TEMPERATURE', value = value)
	resp = HttpResponse()
	resp.status_code = 200
	return resp

def api_get_setted_temperature(request):
	logging.add(request, "GET SETTED_TEMPERATURE")
	item = dbwork.get_last_record(rec_type = 'SETTED_TEMPERATURE')
	return HttpResponse(item.value)

def api_set_setted_temperature(request):
	logging.add(request, "SET SETTED_TEMPERATURE")
	if request.method == 'POST':
		data = request.POST['data']
	else:
		data = request.GET['data']
	param_list = json.loads(data)
	value = param_list['value']
	dbwork.add_record(rec_type = 'SETTED_TEMPERATURE', value = value)
	resp = HttpResponse()
	resp.status_code = 200
	return resp

def api_get_door(request):
	logging.add(request, "GET DOOR")
	item = dbwork.get_last_record(rec_type = 'DOOR')
	return HttpResponse(item.value)

def api_set_door(request):
	logging.add(request, "SET DOOR")
	if request.method == 'POST':
		data = request.POST['data']
	else:
		data = request.GET['data']
	param_list = json.loads(data)
	value = param_list['value']
	dbwork.add_record(rec_type = 'DOOR', value = value)
	ip = dbwork.get_last_record(rec_type = 'IP').value
	req = 'http://' + ip + '/'
	req += 'dooron' if value == '1' else 'dooroff'
	requests.get(req)
	resp = HttpResponse()
	resp.status_code = 200
	return resp

def api_get_light(request):
	logging.add(request, "GET LIGHT")
	item = dbwork.get_last_record(rec_type = 'LIGHT')
	return HttpResponse(item.value)

def api_set_light(request):
	logging.add(request, "SET LIGHT")
	if request.method == 'POST':
		data = request.POST['data']
	else:
		data = request.GET['data']
	param_list = json.loads(data)
	value = param_list['value']
	dbwork.add_record(rec_type = 'LIGHT', value = value)
	ip = dbwork.get_last_record(rec_type = 'IP').value
	req = 'http://' + ip + '/'
	req += 'lighton' if value == '1' else 'lightoff'
	requests.get(req)
	resp = HttpResponse()
	resp.status_code = 200
	return resp

def showlog(request):
	count = request.GET['count']
	resp = "\n"
	list = logging.get_logs(int(count))
	for item in list:
		resp = resp + item.text
	return HttpResponse(resp)


def api_set_randomtemperature(request):
	res = dbwork.get_last_record(rec_type='TEMPERATURE').value
	res = float(res)
	i = (random.randint(0, 100) - 50) / 100.
	res += i
	res = round(res,2)
	requests.post("http://127.0.0.1:8000/api/set/temperature", data={'data' : '{"value":' + str(res) + '}'})
	return HttpResponse('OK')

def api_set_ip(request):
	logging.add(request, "SET IP")
	ip = request.GET['ip']
	dbwork.add_record(rec_type='IP', value=ip)
	return HttpResponse('OK')
