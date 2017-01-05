from .models import Log
import time

def add(request, what):
	text = what
	text = text + "\t" + time.asctime() + "\n"
	text = text + "GET params:" + "\n"
	for name in request.GET:
		text = text + "\t" + name + ":\t" + request.GET[name] + "\n"
	text = text + "POST params:" + "\n"
	for name in request.POST:
		text = text + "\t" + name + ":\t" + request.POST[name] + "\n"
	text = text + "\n"
	log = Log(text = text)
	log.save()

def get_logs(count):
	list = Log.objects.filter()
	return list[len(list) - count:]	
