import socket
import threading
import os
import base64

MAX_CLIENTS=5
mydict = {}
IMAGE_SAVE_PATH = "C:\\Users\\user\\snapshots"
DEBUG = 0

def log(msg):
	if DEBUG:
		print msg
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
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("0.0.0.0", 10000))
	s.listen(100)
	client, addr = s.accept()
	while True:
		log('Waiting for data')
		data = client.recv(3000000)
		log('Got data')
		if not data:
			log('breaking')
			break
		#print data
		arr_data = data.split(',')
		#print arr_data
		userid = arr_data[0]
		snapid = arr_data[1]
		log('From userid: {0}, and snapid: {1}'.format(userid, snapid))
		raw_data = ','.join(arr_data[2:])
		fname = "{0}_{1}.jpg".format(userid, snapid)
		f = open(os.path.join(IMAGE_SAVE_PATH, fname), 'ab')
		f.write(base64.b64decode(raw_data))
		f.close()


def handle_client(client_sock, addr, userid):
	"""
	Handles a client, receive and print
	"""
	log('[*] New Thread for {0}:{1}!'.format(addr[0], addr[1]))
	while True:
		req = client_sock.recv(9999999)
		log('[*] Client {0}:{1} requests {2}'.format(addr[0], addr[1], req))
		# Get a job and send
		if len(mydict[userid]) != 0:
			# we have a job
			myjob = mydict[userid].pop(0)
			client_sock.send(myjob)
		else:
			client_sock.send('nojobs')

		


def main():
	"""
	Main function
	"""
	client_list = []

	log('Welcome to the server!')
	s = listen()
	log('[*] Listening...')

	while True:
		client, addr = s.accept()
		# We've received a connection
		userid = client.recv(1024)
		client_list.append((client, addr))
		log('New client from {0}:{1}, userid={2}'.format(addr[0], addr[1], userid))
		mydict[userid] = ['hey', 'hey']
		client.send('ACK')
		th = threading.Thread(target=handle_client, args=(client,addr,userid,))
		th.start()


if __name__ == '__main__':
	#main()
	handle_snaps_server()