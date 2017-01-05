from .models import Thing, Log, Record

def get_last_record(rec_type):
	item = Record.objects.filter(type = rec_type)
	return item[len(item) - 1]

def add_record(rec_type, value):
	item = Record(type = rec_type, value = value)
	item.save()
