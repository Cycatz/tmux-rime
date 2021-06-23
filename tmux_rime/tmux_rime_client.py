#!/usr/bin/env python
import sys
import argparse

# import socket
# import sys
# import os
# server_address = '/tmp/tmux-rime.test'
# 
# with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
# 	s.connect(server_address)
# 	while True:
# 		s.sendall(b'HelloWorld')
# 		data = s.recv(1024)
# 		print('Received', repr(data))

class TmuxRimeSession:
    pass

class TmuxRimeParser:
    @classmethod
    def __start(cls, args):
        print('Started!')
    @classmethod
    def __exit(cls, args):
        print('Exited')

    @classmethod
    def parse(cls):
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        parser_start = subparser.add_parser('start', help='Start a rime session')
        parser_start.add_argument('-s', type=int, required=True, help='Specify the tmux session id')
        parser_start.set_defaults(func=cls.__start)

        parser_exit = subparser.add_parser('exit', help='Exit a rime session')
        parser_exit.add_argument('-s', type=int, required=True, help='Specify the tmux session id')
        parser_exit.set_defaults(func=cls.__exit)

        args = parser.parse_args()
        args.func(args)

if __name__ == '__main__':
    TmuxRimeParser.parse()
