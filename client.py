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
import subprocess
import getpass
import struct
import win32api


global userid


killSnap = 0
killLock = 0
killStream = 0
DEBUG = 1
SERVER_IP = "192.168.1.101"
IMAGE_SAVE_PATH = "C:\\Users\\" + getpass.getuser() + "\\snapshots"


def log(msg):
	if DEBUG:
		print msg
	return

def setup_folders():
	# Checks if any required folder does not exist
	if not os.path.exists(IMAGE_SAVE_PATH):
		os.makedirs(IMAGE_SAVE_PATH)
	if not os.path.exists(IMAGE_SAVE_PATH + "\\temp"):
		os.makedirs(IMAGE_SAVE_PATH + "\\temp")


def get_stream(userid):
	global killStream
	log("get stream {0}".format(userid))
	# Connect to the stream request handler on the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((SERVER_IP, 8004))

	# Send the requested userid to the server
	s.send(userid)

	log("sent userid")
		
	while True:
		if killStream:
			log('killStream, breaking')
			return
		#log('Waiting for data')
		data = s.recv(300000)
		s.send("okheader")
		#log('Got data')
		if not data:
			log('breaking')
			break

		#print data[0:50]
		arr_data = data.split(',')

		#msg = "{0},{1},{2},{3},{4},{5}".format(userid, image_date, image_hour, image_minute, snapid, encoded_data)
		userid = arr_data[0]
		image_date = arr_data[1]
		image_hour = arr_data[2]
		image_minute = arr_data[3]
		snapid = arr_data[4]
		encoded_len = int(arr_data[5])

		folder_path = os.path.join(IMAGE_SAVE_PATH, userid, image_date, image_hour, image_minute)
		try:
			os.makedirs(folder_path)
		except OSError:
			# Folder exists
			pass

		#log('From userid: {0}, and snapid: {1}'.format(userid, snapid))
		#log('Expecting {0} bytes of data'.format(encoded_len))
		got_encoded = ""
		while len(got_encoded) < encoded_len:
			data = s.recv(300000)
			#log('Got encoded data, len={0}, max={1}'.format(len(data), encoded_len))
			if not data:
				log('breaking encoded')
				break
			got_encoded += data
			#log("now we have {0} from {1}".format(len(got_encoded), encoded_len))

		fname = "{0}.jpg".format(snapid)
		log("writing file {0}".format(fname)0)
		f = open(os.path.join(folder_path, fname), 'ab')
		f.write(base64.b64decode(got_encoded))
		f.close()
		s.send("okfile")
	f.close()

def lockscreen_handler():
	global killLock

	while True:
		if killLock:
			log('Unlocking the client')
			break

		ctypes.windll.user32.LockWorkStation()
		time.sleep(1)

	return


def snap_handler(userid):
	global killSnap
	log('started snap handler')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((SERVER_IP, 10000))
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
		save_path = "{0}\\temp\\MySnapshot_{1}.jpg".format(IMAGE_SAVE_PATH, random.randint(0,99999))
		snapshot.save(save_path)
		#log('got snap, snapid: ' + str(snapid))
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
		try:
			os.remove(save_path)
		except Exception:
			pass

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
	global killLock
	global killSnap
	global killStream

	log("[*] Trying to sync the clock")
	subprocess.call(["python", "set_ntp.py"])
	setup_folders()

	userid = random.randint(1,10001)
	log('userid ' + str(userid))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((SERVER_IP, 8002))
			log('connected')
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
					killSnap = 0
					threading.Thread(target=snap_handler, args=(userid,)).start()
				elif req == 'lockscreen':
					threading.Thread(target=lockscreen_handler).start()
				elif req == 'unlockscreen':
					killLock = 1
				elif req == 'stopsnap':
					killSnap = 1
				elif req == 'stopstream':
					log("stopstream")
					killStream = 1
					os.system("taskkill /f /im teacherhelper_view.exe")
					os.system("taskkill /f /im teacherhelper_view_x64.exe")
				elif req.startswith('stream'):
					killStream = 0
					stream_userid = req.split(';')[1]
					threading.Thread(target=get_stream, args=(stream_userid,)).start()
					# TODO Start the view.exe process with stream_userid
					subprocess.call(["C:\\Windows\\teacherhelper_view_x64.exe", stream_userid])
				elif req == 'nojobs':
					log('no jobs for me!')
		except Exception:
			log('Disconnected from server, restart')
			continue
	

if __name__ == '__main__':
	main()
