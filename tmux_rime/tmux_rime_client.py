#!/usr/bin/env python
import socket
import argparse

class TmuxRimeParser:
    def __init__(self, client):
        self.client = client

    def start(self, args):
        self.client.start(session_id=args.session_id)

    def exit(self, args):
        self.client.exit(session_id=args.session_id)

    def key(self, args):
        self.client.key(session_id=args.session_id,
                        key=args.key,
                        modifier=args.modifier)
    def output(self, args):
        self.client.output(session_id=args.session_id)

    def parse(self):
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        parser_start = subparser.add_parser('start', help='Start a rime session')
        parser_start.add_argument('-s', '--session-id', type=int, required=True, help='Specify the tmux session id')
        parser_start.set_defaults(func=self.start)

        parser_key = subparser.add_parser('key', help='Send keys to a session')
        parser_key.add_argument('-s', '--session-id', type=int, required=True, help='Specify the tmux session id')
        parser_key.add_argument('-k', '--key', type=str, required=True, help='Specify the key')
        parser_key.add_argument('-m', '--modifier', type=str, help='Specify the key modifier')
        parser_key.set_defaults(func=self.key)


        parser_output = subparser.add_parser('output', help='Get inserted text')
        parser_output.add_argument('-s', '--session-id', type=int, required=True, help='Specify the tmux session id')
        parser_output.set_defaults(func=self.output)

        parser_exit = subparser.add_parser('exit', help='Exit a rime session')
        parser_exit.add_argument('-s', '--session-id', type=int, required=True, help='Specify the tmux session id')
        parser_exit.set_defaults(func=self.exit)

        args = parser.parse_args()
        args.func(args)

class TmuxRimeClient:
    def __init__(self):
        self.server_address = '/tmp/tmux-rime.rime'

    def send(self, data, recv=False):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            try:
                s.sendall(data)
                if recv:
                    res = s.recv(1024)
                    return res
            finally:
                s.close()

    def start(self, session_id):
        self.send('start {}'.format(session_id).encode('utf-8'))
        print('Start session {}'.format(session_id))

    def exit(self, session_id):
        self.send('exit {}'.format(session_id).encode('utf-8'))
        print('Exit session {}'.format(session_id))

    def key(self, session_id, key, modifier):
        status_text = self.send('key {} {} {}'.format(session_id, key, modifier)
                                         .encode('utf-8'), True)

        inserted_text = self.send('output {}'.format(session_id).encode('utf-8'), True)

        if status_text is not None:
            print(status_text.decode('utf-8'))

        if inserted_text is not None:
            print(inserted_text.decode('utf-8'))

    def output(self, session_id):
        res = self.send('output {}'.format(session_id).encode('utf-8'), True)
        if res is not None:
            print(res.decode('utf-8'))

if __name__ == '__main__':
    client = TmuxRimeClient()
    parser = TmuxRimeParser(client)
    parser.parse()
