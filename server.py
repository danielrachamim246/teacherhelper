import socket
import sys
import threading
import os
import base64
import Queue
import datetime
import time
import getpass
import struct
import win32api
import ctypes
import subprocess
import shutil

MAX_CLIENTS=5
mydict = {}
IMAGE_SAVE_PATH = "C:\\Users\\" + getpass.getuser() + "\\snapshots"
DEBUG = 1

def log(msg):
	if DEBUG:
		print msg
		flog = open('server.log', 'a')
		flog.write("{0}\n".format(msg))
		flog.close()
	return

def delete_history_snaps():
	usersdir = os.listdir(IMAGE_SAVE_PATH)
	todayobj = datetime.datetime.now()
	deltaobj = datetime.timedelta(days=2)
	for userdir in usersdir:
		if userdir == "temp":
			continue
		path = "{0}\\{1}".format(IMAGE_SAVE_PATH, userdir)
		datesdir = os.listdir(path)
		for datedir in datesdir:
			# For each folder
			diryear = int(datedir.split('-') [0])
			dirmonth = int(datedir.split('-') [1])
			dirday = int(datedir.split('-') [2])
			dirdateobj = datetime.datetime(diryear, dirmonth, dirday)

			# Do we want to delete?
			if (todayobj - dirdateobj) > deltaobj:
				# TODO REALLY DELETE
				delpath = "{0}\\{1}\\{2}".format(IMAGE_SAVE_PATH, userdir, datedir)
				print 'delete! ' + delpath
				shutil.rmtree(delpath)
				print 'deleted'


def teacher_put_cmd(teacher_cmd, client_cmd):
	sp = teacher_cmd.split(',')
	if len(sp) != 2:
		# log debug not a valid command
		return 'InvalidCommand'
	try:
		q = mydict[int(sp[1])]
		q.put(client_cmd)
		q.task_done()
	except KeyError: 	
		return "InvalidClient"
	
	return 'Executed'


def handle_teacher(s=None):
	if s is None:
		return
	while True:
		try:
			cmd = s.recv(3000000)
		except Exception:
			return
		log('MGMT | Teacher | received {0}'.format(cmd))
		if cmd == 'getClient':
			# return a string with all the clients, seperated by ","
			clientList = ",".join(str(item) for item in mydict.keys())
			print clientList
			if clientList == "":
				s.send("None")
			else:
				s.send(clientList)
			continue

		elif cmd.startswith('lockClient'):
			s.send(teacher_put_cmd(cmd, 'lockscreen'))
			continue

		elif cmd.startswith('unlockClient'):
			s.send(teacher_put_cmd(cmd, 'unlockscreen'))
			continue

		elif cmd.startswith('requestStreamClient'):
			s.send(teacher_put_cmd(cmd, 'snap'))
			continue

		elif cmd.startswith('requestStopStreamClient'):
			s.send(teacher_put_cmd(cmd, 'stopsnap'))
			continue

		# Relevant for the clients themselves, to get the screen of the teacher
		# getlive,targetuserid;streamfromid
		elif cmd.startswith('getLiveStreamClient'):
			stream_userid = cmd.split(',')[1].split(';')[1]
			s.send(teacher_put_cmd(cmd.split(';')[0], 'stream;{0}'.format(stream_userid)))
			continue

		elif cmd.startswith('stopLiveStreamClient'):
			s.send(teacher_put_cmd(cmd, 'stopstream'))
			continue

		else:
			s.send('InvalidCommand')
			continue
def open_stream_file(filename):
	try:
		f = open(filename, 'rb')
		return f
	except Exception:
		log("cannot open file {0}".format(filename))
		return None

def get_stream_send(s=None, userid=0):
	snapid = 0
	image_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
	image_date = image_timestamp.split('T')[0]
	image_hour = image_timestamp.split('T')[1].split(":")[0]
	image_minute = image_timestamp.split('T')[1].split(":")[1]
	folder_path = os.path.join(IMAGE_SAVE_PATH, str(userid), image_date, image_hour, image_minute)
	while True:
		#log("start of main loop get_stream_send")
		filename = os.path.join(folder_path, "{0}.jpg".format(snapid))
		if not os.path.exists(filename):
			image_new_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
			if image_timestamp == image_new_timestamp:
				#log("start main continue, {0}".format(filename))
				continue
				#log("after continue")
			snapid = 0

		#log("before file open {0}".format(filename))
		#while True:
		f = open_stream_file(filename)
		if f is None:
			continue
		while True:
			#log('Reading from snap')
			raw_data = f.read(50000000)
			if not raw_data:
				log('breaking')
				break
			encoded_data = base64.b64encode(raw_data)
			msg = "{0},{1},{2},{3},{4},{5}".format(userid, image_date, image_hour, image_minute, snapid, len(encoded_data))
			s.send(msg)
			s.recv(100)
			#log("sent header, with ack")
			s.send(encoded_data)
			#log('Sent snap')
			s.recv(100)
			#log("sent data, with ack")
		f.close()

		image_new_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
		if image_new_timestamp != image_timestamp:
			image_timestamp = image_new_timestamp
			image_date = image_timestamp.split('T')[0]
			image_hour = image_timestamp.split('T')[1].split(":")[0]
			image_minute = image_timestamp.split('T')[1].split(":")[1]
			folder_path = os.path.join(IMAGE_SAVE_PATH, str(userid), image_date, image_hour, image_minute)
			snapid = 0
		else:
			snapid += 1


def handle_get_stream(s=None):
	if s is None:
		return
	while True:
		try:
			userid = int(s.recv(300))
			log('GET_STREAM | Handler | userid={0}'.format(userid))
			get_stream_send(s, userid)
		except Exception:
			log('stream disconnected from {0}'.format(userid))
			return
		

def handle_get_stream_server():
	# Listens of 8004
	# Sends photos of the teacher (userid=0), the latest (live)
	
	s = listen(port=8004)
	while True:
		r_sock, addr = s.accept()
		log('GET_STREAM | New Connection')
		# We've received a connection
		th = threading.Thread(target=handle_get_stream, args=(r_sock,))
		th.start()

	return



def handle_mgmt_server():
	# Listens of 8003
	# Handles requests 
	
	s = listen(port=8003)
	while True:
		teacher_sock, addr = s.accept()
		log('MGMT | New Connection')
		# We've received a connection
		th = threading.Thread(target=handle_teacher, args=(teacher_sock,))
		th.start()

	return

def listen(port=8002):
	"""
	Listening on socket and returns the socket
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0", int(port)))
	s.listen(MAX_CLIENTS)
	return s

def handle_snap_server_sock(client):
	try:
		while True:
			#log('Waiting for data')
			data = client.recv(300000)
			client.send("okheader")
			#log('Got data')
			if not data:
				#log('breaking')
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
			while len(got_encoded) != encoded_len:
				data = client.recv(300000)
				#log('Got encoded data, len={0}, max={1}'.format(len(data), encoded_len))
				if not data:
					log('breaking encoded')
					break
				got_encoded += data
				#log("now we have {0} from {1}".format(len(got_encoded), encoded_len))

			fname = "{0}.jpg".format(snapid)
			#log("writing file {0}".format(fname))
			f = open(os.path.join(folder_path, fname), 'ab')
			f.write(base64.b64decode(got_encoded))
			f.close()
			client.send("okfile")
	except Exception:
		return


def handle_snaps_server():
	log('SNAP | Listening...')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0", 10000))
	s.listen(100)
	while True:
		log('SNAP | Waiting for Another Connection')
		client, addr = s.accept()
		log('SNAP | Accepted Connection')
		threading.Thread(target=handle_snap_server_sock, args=(client,)).start()
	
	


def handle_client(client_sock, addr, userid):
	"""
	Handles a client, receive and print
	"""
	log('[*] New Thread for {0}:{1}!'.format(addr[0], addr[1]))
	while True:
		try:
			req = client_sock.recv(9999999)

			log('[*] Client {0}:{1} requests {2}'.format(addr[0], addr[1], req))
			# Get a job and send
			try:
				job = mydict[userid].get(True, 1)
			except Queue.Empty:
				client_sock.send('nojobs')
				continue

			if job is not None:
				# we have a job
				client_sock.send(job)
			else:
				client_sock.send('nojobs')
		except Exception:
			del mydict[userid]
			log("client {0} disconnected!".format(userid))
			return
		

def setup_folders():
	# Checks if any required folder does not exist
	if not os.path.exists(IMAGE_SAVE_PATH):
		os.makedirs(IMAGE_SAVE_PATH)
	if not os.path.exists(IMAGE_SAVE_PATH + "\\temp"):
		os.makedirs(IMAGE_SAVE_PATH + "\\temp")

# TODO Server should clear snapshot history for other days
def main():
	"""
	Main function
	"""
	setup_folders()
	log("[*] Trying to sync the clock")
	subprocess.call(["python", "set_ntp.py"])
	client_list = []

	log('Welcome to the server!')
	s = listen(8002)
	delete_history_snaps()
	log('[*] Listening...')

	# Creates an handler to the snaps server
	threading.Thread(target=handle_snaps_server).start()
	threading.Thread(target=handle_mgmt_server).start()
	threading.Thread(target=handle_get_stream_server).start()

	while True:
		client, addr = s.accept()
		# We've received a connection
		try:
			userid = client.recv(1024)
		except Exception:
			continue

		client_list.append((client, addr))
		log('New client from {0}:{1}, userid={2}'.format(addr[0], addr[1], userid))
		
		# Create a queue for the user
		mydict[int(userid)] = Queue.Queue()
		client.send('ACK')
		# TODO Thread Pool
		th = threading.Thread(target=handle_client, args=(client,addr,int(userid),))
		th.start()


if __name__ == '__main__':
	main()