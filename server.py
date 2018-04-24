import socket
import threading
import os
import base64
import Queue

MAX_CLIENTS=5
mydict = {}
IMAGE_SAVE_PATH = "C:\\Users\\user\\snapshots"
DEBUG = 1

def log(msg):
	if DEBUG:
		print msg
	return

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
		cmd = s.recv(3000000)
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

		elif cmd.startswith('requestStreamClient'):
			s.send(teacher_put_cmd(cmd, 'snap'))
			continue

		elif cmd.startswith('getLiveStreamClient'):
			s.send(teacher_put_cmd(cmd, 'snap'))
			continue

		else:
			s.send('InvalidCommand')
			continue


def get_folder_path_live_stream(userid, image_timestamp):
	image_date = image_timestamp.split('T')[0]
	image_hour = image_timestamp.split('T')[1].split(":")[0]
	image_minute = image_timestamp.split('T')[1].split(":")[1]
	folder_path = os.path.join(IMAGE_SAVE_PATH, userid, image_date, image_hour, image_minute)
	return folder_path

def get_stream_send(s=None):
	# TODO Start from the max file number and not from zero
	snapid = 0
	image_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
	folder_path = get_folder_path_live_stream(0, image_timestamp)
	while True:
		filename = os.path.join(folder_path, "{0}.jpg".format(snapid))
		if not os.path.exists(filename):
			image_new_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
			if image_timestamp == image_new_timestamp:
				continue
			snapid = 0

		f = open(save_path, 'rb')
		while True:
			log('Reading from snap')
			raw_data = f.read(50000000)
			if not raw_data:
				log('breaking')
				break
			encoded_data = base64.b64encode(raw_data)
			msg = "{0}".format(len(encoded_data))
			s.send(msg)
			time.sleep(0.1)
			s.send(encoded_data)
			#time.sleep(0.1)
			log('Sent snap')
		f.close()


def handle_get_stream(s=None):
	if s is None:
		return
	while True:
		userid = int(s.recv(300))
		log('GET_STREAM | Handler | userid={0}'.format(userid))
		if userid != 0:
			log('ERROR: Client requested another user than the teacher')
			return
		get_stream_send(s)
		

def handle_get_stream_server():
	# Listens of 8004
	# Sends photos of the teacher (userid=0), the latest (live)
	
	s = listen(port=8004)
	while True:
		r_sock, addr = s.accept()
		log('GET_STREAM | New Connection')
		# We've received a connection
		th = threading.Thread(target=handle_teacher, args=(teacher_sock,))
		th.start()

	return



def handle_mgmt_server():
	# Listens of 8003
	# Handles requests 
	# TODO how to share commands between the clients server and the mgmt server
	
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

def handle_snaps_server():
	log('SNAP | Listening...')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0", 10000))
	s.listen(100)
	client, addr = s.accept()
	log('SNAP | Accepted Connection')
	# TODO: multi threading support
	
	while True:
		log('Waiting for data')
		data = client.recv(300000)
		log('Got data')
		if not data:
			log('breaking')
			break

		print data[0:50]
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

		log('From userid: {0}, and snapid: {1}'.format(userid, snapid))
		log('Expecting {0} bytes of data'.format(encoded_len))
		got_encoded = ""
		while len(got_encoded) != encoded_len:
			data = client.recv(300000)
			log('Got encoded data, len={0}, max={1}'.format(len(data), encoded_len))
			if not data:
				log('breaking encoded')
				break
			got_encoded += data
			log("now we have {0} from {1}".format(len(got_encoded), encoded_len))

		fname = "{0}.jpg".format(snapid)
		log("writing file {0}".format(fname))
		f = open(os.path.join(folder_path, fname), 'ab')
		f.write(base64.b64decode(got_encoded))
		f.close()


def handle_client(client_sock, addr, userid):
	"""
	Handles a client, receive and print
	"""
	log('[*] New Thread for {0}:{1}!'.format(addr[0], addr[1]))
	while True:
		try:
			req = client_sock.recv(9999999)
		except Exception:
			del mydict[userid]
			log("client {0} disconnected!".format(userid))
			return

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

		

# TODO Server should clear snapshot history for other days
def main():
	"""
	Main function
	"""
	client_list = []

	log('Welcome to the server!')
	s = listen(8002)
	log('[*] Listening...')

	# Creates an handler to the snaps server
	threading.Thread(target=handle_snaps_server).start()
	threading.Thread(target=handle_mgmt_server).start()

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