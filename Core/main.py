import time
import zmq
import threading
import time
from dexter import Dexter
from gesture import handDetection

def zmq_sock():
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://127.0.0.1:5555")

	while True:

		#  Wait for incoming request from client
		print("Listening...")
		message = socket.recv()
		print("Received request: %s\nSending response" % message)

		#  Do some other stuff
		time.sleep(1)

		#  Send reply back to client
		socket.send_string("What it do")


if __name__ == '__main__':
	#Establish a socket to start listening for incoming messages on
	zmq_sock()