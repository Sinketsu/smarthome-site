from .models import Thing, Log, Record, Mobile, Chart_r

def get_salt():
	return get_last_record(rec_type = 'HASH_SALT')

def get_default_salt():
	return get_last_record(rec_type = 'DEFAULT_HASH_SALT')

def get_last_record(rec_type):
	item = Record.objects.filter(type = rec_type)
	return item[len(item) - 1]

def add_record(rec_type, value):
	item = Record(type = rec_type, value = value)
	item.save()

def set_mobile_password(name, key):
	item = Mobile(name = name, password = key)
	item.save()

def get_chart():
	item = Chart_r.objects.all()
	return item[len(item) - 1]
