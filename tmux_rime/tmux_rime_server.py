#!/usr/bin/env python

import socket
import sys
import os
from rime import *

class TmuxRimeSession:
	def __init__(self):
		self.rime = tmux_rime_init()
	def start(self):
		tmux_rime_start(self.rime, False)




server_address = '/tmp/tmux-rime.test'

try:
	os.unlink(server_address)
except OSError:
	if os.path.exists(server_address):
		raise


with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
	s.bind(server_address)
	s.listen()

	while True:
		print('Waiting for a connection...')
		conn, addr = s.accept()
		data = conn.recv(1024)
		if not data:
			break
		print('Recieved ' + repr(data) + '!')
		conn.sendall(data)
