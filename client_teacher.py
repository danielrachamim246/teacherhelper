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
import getpass

global userid


killSnap = 0
killLock = 0
DEBUG = 1
IMAGE_SAVE_PATH = "C:\\Users\\" + getpass.getuser() + "\\snapshots"

def log(msg):
	if DEBUG:
		print msg
	return

def snap_handler(userid):
	global killSnap
	log('started snap handler')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 10000))
	snapid = 0
	image_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
	image_date = image_timestamp.split('T')[0]
	image_hour = image_timestamp.split('T')[1].split(":")[0]
	image_minute = image_timestamp.split('T')[1].split(":")[1]
	print datetime.datetime.now().isoformat()
	while True:
		if killSnap:
			log('killSnap, breaking')
			return
		snapshot = ImageGrab.grab() # TODO Lower quality
		save_path = "C:\\Users\\" + getpass.getuser() + "\\snapshots\\temp\\MySnapshot_{0}.jpg".format(random.randint(0,99999))
		snapshot.save(save_path)
		log('got snap, snapid: ' + str(snapid))
		# Send
		f = open(save_path, 'rb')

		while True:
			#log('Reading from snap')
			raw_data = f.read(500000)
			if not raw_data:
				#log('breaking')
				break
			encoded_data = base64.b64encode(raw_data)
			msg = "{0},{1},{2},{3},{4},{5}".format(userid, image_date, image_hour, image_minute, snapid, len(encoded_data))
			s.send(msg)
			s.recv(100)
			s.send(encoded_data)
			s.recv(100)
			#log('Sent snap')

		# finish, remove the file
		f.close()
		os.remove(save_path)

		# Check for new variables for the next file
		image_new_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
		if image_new_timestamp != image_timestamp:
			log("changed time")
			image_timestamp = image_new_timestamp
			image_date = image_timestamp.split('T')[0]
			image_hour = image_timestamp.split('T')[1].split(":")[0]
			image_minute = image_timestamp.split('T')[1].split(":")[1]
			snapid = 0
		else:
			snapid += 1

	print datetime.datetime.now().isoformat()


def setup_folders():
	# Checks if any required folder does not exist
	if not os.path.exists(IMAGE_SAVE_PATH):
		os.makedirs(IMAGE_SAVE_PATH)
	if not os.path.exists(IMAGE_SAVE_PATH + "\\temp"):
		os.makedirs(IMAGE_SAVE_PATH + "\\temp")

def main():
	# TODO Allow killing
	setup_folders()
	snap_handler(0)

if __name__ == '__main__':
	main()