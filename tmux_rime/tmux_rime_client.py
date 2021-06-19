#!/usr/bin/env python

import socket
import sys
import os
server_address = '/tmp/tmux-rime.test'

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
	s.connect(server_address)
	while True:
		s.sendall(b'HelloWorld')
		data = s.recv(1024)
		print('Received', repr(data))
