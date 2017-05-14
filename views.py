from django.http import HttpResponse, FileResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Log, Thing, Record, Chart_r 
from . import dbwork
from . import logging
import socket
import time
import json
import random
import datetime
import requests
import pygame
from Crypto import Random
import base64
import urllib
import re
import hashlib

def auth(request):
	logging.add(request, "AUTH")
	if request.user.is_authenticated():
		session_cipher_key = Random.get_random_bytes(32)
		session_cipher_key = base64.b64encode(session_cipher_key).decode('utf-8')
		dbwork.set_mobile_password('MOBILE', session_cipher_key)
		return HttpResponse('{"key":\"' + session_cipher_key + '\"}')
	if request.method != 'POST':
		return HttpResponse('Not supported, sorry')
	username = request.POST['username']
	passwd = request.POST['password']

	user = authenticate(username = username, password = passwd)
	if user is not None:
		if user.is_active:
			login(request, user)
			session_cipher_key = Random.get_random_bytes(32)
			session_cipher_key = base64.b64encode(session_cipher_key).decode('utf-8')
			dbwork.set_mobile_password('MOBILE', session_cipher_key)
			resp = HttpResponse('{"key":\"' + session_cipher_key + '\"}')
			resp.status_code = 200
			return resp
		else:
			resp = HttpResponse('User is disable')
			resp.status_code = 403
			return resp
	else:
		resp = HttpResponse('Invalid login/password')
		resp.status_code = 401
		return resp

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

def not_authorized():
	resp = HttpResponse('Not authorized')
	resp.status_code = 401
	return resp

def not_valid():
	resp = HttpResponse('Request is invalid')
	resp.status_code = 400
	return resp

def check_hash(data, hash):
	sha384 = hashlib.sha384()
	salt = dbwork.get_salt().value
	default_salt = dbwork.get_default_salt().value
	c_hash = hashlib.sha384((salt + data).encode()).hexdigest()
	def_c_hash = hashlib.sha384((default_salt + data).encode()).hexdigest()
	if hash == c_hash or hash == def_c_hash:
		return True
	else:
		return False

def photo(request):
	if request.user.is_authenticated():
		try:
			rnd = request.GET['rnd']
			hash = request.GET['hash']
			if check_hash(rnd, hash):
				time.sleep(.500)
				res = urllib.request.urlopen('http://127.0.0.1:8080/?action=snapshot')
				return FileResponse(res, content_type='image/jpg')
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()	
	
def camera(request):
	if request.user.is_authenticated():
		return render_to_response('camera.html', {})
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


def chart_add(request):
	rec = Chart_r()
	rec.n0 = int(request.POST['n0'])
	rec.n1 = int(request.POST['n1'])
	rec.n2 = int(request.POST['n2'])
	rec.n3 = int(request.POST['n3'])
	rec.n4 = int(request.POST['n4'])
	rec.n5 = int(request.POST['n5'])
	rec.n6 = int(request.POST['n6'])
	rec.n7 = int(request.POST['n7'])
	rec.n8 = int(request.POST['n8'])
	rec.n9 = int(request.POST['n9'])
	rec.n10 = int(request.POST['n10'])
	rec.n11 = int(request.POST['n11'])
	rec.n12 = int(request.POST['n12'])
	rec.n13 = int(request.POST['n13'])
	rec.n14 = int(request.POST['n14'])
	rec.n15 = int(request.POST['n15'])
	rec.n16 = int(request.POST['n16'])
	rec.n17 = int(request.POST['n17'])
	rec.n18 = int(request.POST['n18'])
	rec.n19 = int(request.POST['n19'])

	rec.save()
	return HttpResponse()

def chart_update(request):
	rec = dbwork.get_chart()
	return HttpResponse('{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(rec.n0, rec.n1, rec.n2, rec.n3, rec.n4, rec.n5, 
									rec.n6, rec.n7, rec.n8, rec.n9, rec.n10, rec.n11, rec.n12, rec.n13,
									rec.n14, rec.n15, rec.n16, rec.n17, rec.n18, rec.n19))

def chart(request):
	return render_to_response('chart.html', {})


def get_weather(request):
	if request.user.is_authenticated():
		try:
			rnd = request.GET['rnd']
			hash = request.GET['hash']
			if check_hash(rnd, hash):
				body = requests.get('https://yandex.ru/pogoda/ufa').text
				temp = re.findall('<span class="wind-speed">\S*\s\S*</span>', body)
				wind = temp[0][25:-7]
				temp = re.findall('>\w\w</abbr><i class=', body)
				wind_direction = temp[0][1:-16]
				temp = re.findall('<span class="current-weather__comment">[\s\S]*</span><div class="current-weather', body)
				comment = temp[0][39:-34]
				temp = re.findall('<div class="current-weather__thermometer current-weather__thermometer_type_now">[\s\S]*</div></span><span class="current-weather__col current-weather__col_type_nowcast">', body)
				temperature = temp[0][80:-85]
				text = '{' + '"temperature" : "{}", "comment" : "{}", "wind_velocity" : "{}", "wind_direction" : "{}"'.format(temperature, comment, wind, wind_direction) + '}' 
				return HttpResponse(text)
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()		

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

def api_mobile_get_count_light(request):
	logging.add(request, "MOBILE GET COUNT LIGHT")
	if request.user.is_authenticated():
		try:
			rnd = request.GET['rnd']
			hash = request.GET['hash']
			if check_hash(rnd, hash):
				spotlight = dbwork.get_last_record(rec_type = 'SPOTLIGHT').value
				light = dbwork.get_last_record(rec_type = 'LIGHT').value
				active = int(spotlight) + int(light)
				response = '{' + '"active":{}, "all":{}'.format(str(active), 2) + '}'
				return HttpResponse(response)
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()

def api_mobile_get_count_door(request):
        logging.add(request, "MOBILE GET COUNT DOOR")
        if request.user.is_authenticated():
                try:
                        rnd = request.GET['rnd']
                        hash = request.GET['hash']
                        if check_hash(rnd, hash):
                                door = dbwork.get_last_record(rec_type = 'DOOR').value
                                response = '{' + '"active":{}, "all":{}'.format(door, 1) + '}'
                                return HttpResponse(response)
                        else:
                                return not_authorized()
                except BaseException:
                        return not_valid()
        else:
                return not_authorized()


def api_mobile_get_spotlight(request):
	logging.add(request, "MOBILE GET SPOTLIGHT")
	if request.user.is_authenticated():
		try:
			rnd = request.GET['rnd']
			hash = request.GET['hash']
			if check_hash(rnd, hash):
				item = dbwork.get_last_record(rec_type = 'SPOTLIGHT')
				return HttpResponse(item.value)
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()

def api_mobile_set_spotlight(request):
	logging.add(request, "MOBILE SET SPOTLIGHT")
	if request.user.is_authenticated():
		try:
			data = request.POST['data']
			hash = request.POST['hash']
			if check_hash(data, hash):
				param_list = json.loads(data)
				value = param_list['value']
				dbwork.add_record(rec_type = 'SPOTLIGHT', value = value)

				ip = dbwork.get_last_record(rec_type = 'IP').value
				if ip != 'none':
					req = 'http://' + ip + '/'
					req += 'spotlighton' if value == '1' or value == 1 else 'spotlightoff'
					requests.get(req)

				return HttpResponse()
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()


def api_mobile_get_light(request):
	logging.add(request, "MOBILE GET LIGHT")
	if request.user.is_authenticated():
		try:
			rnd = request.GET['rnd']
			hash = request.GET['hash']
			if check_hash(rnd, hash):
				item = dbwork.get_last_record(rec_type = 'LIGHT')
				return HttpResponse(item.value)
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()

def api_mobile_set_light(request):
	logging.add(request, "MOBILE SET LIGHT")
	if request.user.is_authenticated():
		try:
			data = request.POST['data']
			hash = request.POST['hash']
			if check_hash(data, hash):
				param_list = json.loads(data)
				value = param_list['value']
				dbwork.add_record(rec_type = 'LIGHT', value = value)

				ip = dbwork.get_last_record(rec_type = 'IP').value
				if ip != 'none':
					req = 'http://' + ip + '/'
					req += 'lighton' if value == '1' or value == 1 else 'lightoff'
					requests.get(req)

				return HttpResponse()
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()


def api_mobile_get_door(request):
	logging.add(request, "MOBILE GET DOOR")
	if request.user.is_authenticated():
		try:
			rnd = request.GET['rnd']
			hash = request.GET['hash']
			if check_hash(rnd, hash):
				item = dbwork.get_last_record(rec_type = 'DOOR')
				return HttpResponse(item.value)
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()

def api_mobile_set_door(request):
	logging.add(request, "MOBILE SET DOOR")
	if request.user.is_authenticated():
		try:
			data = request.POST['data']
			hash = request.POST['hash']
			if check_hash(data, hash):
				param_list = json.loads(data)
				value = param_list['value']
				dbwork.add_record(rec_type = 'DOOR', value = value)
				
				ip = dbwork.get_last_record(rec_type = 'IP').value
				if ip != 'none':
					req = 'http://' + ip + '/'
					req += 'dooron' if value == '1' or value == 1 else 'dooroff'
					requests.get(req)

				return HttpResponse()
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()


def api_mobile_get_setted_temperature(request):
	logging.add(request, "MOBILE GET SETTED_TEMPERATURE")
	if request.user.is_authenticated():
		try:
			rnd = request.GET['rnd']
			hash = request.GET['hash']
			if check_hash(rnd, hash):
				item = dbwork.get_last_record(rec_type = 'SETTED_TEMPERATURE')
				return HttpResponse(item.value)
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized() 		

def api_mobile_set_setted_temperature(request):
	logging.add(request, "MOBILE SET SETTED_TEMPERATURE")
	if request.user.is_authenticated():
		try:
			data = request.POST['data']
			hash = request.POST['hash']
			if check_hash(data, hash):
				param_list = json.loads(data)
				value = param_list['value']
				dbwork.add_record(rec_type = 'SETTED_TEMPERATURE', value = value)
				return HttpResponse()
			else:
				return not_authorized()
		except BaseException:
			return not_valid()
	else:
		return not_authorized()


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
	if ip != 'none':
		req = 'http://' + ip + '/data?data='
		req += 'P10' if value == '1' or value == 1 else 'P11'
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
	if ip != 'none':	
		req = 'http://' + ip + '/data?data='
		req += 'P00' if value == '1' or value == 1 else 'P01'
		requests.get(req)

	resp = HttpResponse()
	resp.status_code = 200
	return resp

def api_get_spotlight(request):
	logging.add(request, "GET SPOTLIGHT")
	if request.user.is_authenticated():
		#check the hash
		item = dbwork.get_last_record(rec_type='SPOTLIGHT')
		return HttpResponse(item.value)
	else:
		resp = HttpResponse('Not authorized')
		resp.status_code = 401
		return resp		

def api_set_spotlight(request):
	logging.add(request, "SET SPOTLIGHT")
	if request.user.is_authenticated():
		data = request.POST['data']
		# check the hash
		param_list = json.loads(data)
		value = param_list['value']
		dbwork.add_record(rec_type = 'SPOTLIGHT', value = value)
		
		ip = dbwork.get_last_record(rec_type = 'IP').value
		if ip != 'none':
			#sending request
			pass
		resp = HttpResponse()
		resp.status_code = 200
		return resp
	else:
		resp = HttpResponse('Not authorized')
		resp.status_code = 401
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

def music_play(request):
	pygame.init()
	pygame.mixer.init()
	l = random.randint(1,3)
	music = '/music' + str(l) + '.mp3'
	pygame.mixer.music.load(music)
	pygame.mixer.music.play()
	return HttpResponse()

def music_stop(request):
	pygame.mixer.music.stop()
	return HttpResponse()	
