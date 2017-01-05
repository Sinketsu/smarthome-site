from django.db import models

class Log(models.Model):
	text = models.TextField()
	time = models.DateField(auto_now = True)

class Thing(models.Model):
	type = models.CharField(max_length = 50)
	crypto_key = models.CharField(max_length = 40)
	
	TYPE_CONNECTION = (
		('bl', 'BLUETOOTH'),
		('wf', 'WIFI'),
		('rd', 'RADIO_433')
	)
	conn_type = models.CharField(max_length=2,
				choices=TYPE_CONNECTION, 
				default="wf")

	ip_addr = models.GenericIPAddressField()
	port = models.IntegerField()

	bluetooth_name = models.CharField(max_length = 40)
	channel = models.IntegerField()
	
class Record(models.Model):
	type = models.CharField(max_length = 50)
	value = models.CharField(max_length = 30)
	time = models.DateField(auto_now = True)
