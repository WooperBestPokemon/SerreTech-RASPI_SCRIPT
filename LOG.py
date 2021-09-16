from datetime import datetime
import sys

def write_log(file_name, text_string):

	file_object = open('/home/pi/scripts/logs/{}'.format(file_name), 'a')

	file_object.write('----------  {}  ----------'.format(datetime.now()))
	for x in text_string:
		file_object.write("{}\n".format(x))
		
	file_object.write('')
	file_object.close()
