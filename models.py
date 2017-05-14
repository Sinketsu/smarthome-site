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

class Chart_r(models.Model):
	n0 = models.IntegerField()
	n1 = models.IntegerField()
	n2 = models.IntegerField()
	n3 = models.IntegerField()
	n4 = models.IntegerField()
	n5 = models.IntegerField()
	n6 = models.IntegerField()
	n7 = models.IntegerField()
	n8 = models.IntegerField()
	n9 = models.IntegerField()
	n10 = models.IntegerField()
	n11 = models.IntegerField()
	n12 = models.IntegerField()
	n13 = models.IntegerField()
	n14 = models.IntegerField()
	n15 = models.IntegerField()
	n16 = models.IntegerField()
	n17 = models.IntegerField()
	n18 = models.IntegerField()
	n19 = models.IntegerField()

	
class Record(models.Model):
	type = models.CharField(max_length = 50)
	value = models.CharField(max_length = 30)
	time = models.DateField(auto_now = True)

class Mobile(models.Model):
	name = models.CharField(max_length = 50)
	password = models.CharField(max_length = 70)
	hash_salt = models.CharField(max_length = 70)
