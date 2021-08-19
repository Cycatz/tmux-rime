#!/usr/bin/env python
import os
import sys
import logging
import socket
import argparse


# Fix the FIFO variable for testing
TMUX_RIME_FIFO = '/tmp/tmux-rime.client'


def init_logging():
    logging_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    logging_path = os.path.join(logging_dir, 'tmux_rime_client.log')
    logging.basicConfig(filename=logging_path,
                        format='[%(asctime)s] %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        level=logging.INFO)


class TmuxRimeParser:
    def __init__(self, client):
        self.client = client

    def start_session(self, args):
        self.client.start_session()

    def exit_session(self, args):
        self.client.exit_session()

    def send_key(self, args):
        self.client.send_key(key=args.key,
                             modifier=args.modifier)

    def delete_char(self, args):
        self.client.delete_char()

    def commit_raw(self, args):
        self.client.commit_raw()

    def output(self, args):
        self.client.output()

    def parse(self):
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        parser_start = subparser.add_parser('start', help='Start a rime session')
        parser_start.set_defaults(func=self.start_session)

        parser_key = subparser.add_parser('key', help='Send keys to a session')
        parser_key.add_argument('-k', '--key', type=str, required=True, help='Specify the key')
        parser_key.add_argument('-m', '--modifier', type=str, help='Specify the key modifier')
        parser_key.set_defaults(func=self.send_key)

        parser_delete_char = subparser.add_parser('delete-char',
                                                  help='Delete a char')
        parser_delete_char.set_defaults(func=self.delete_char)

        parser_commit_raw = subparser.add_parser('commit-raw',
                                                 help='Commit the raw input')
        parser_commit_raw.set_defaults(func=self.commit_raw)

        parser_output = subparser.add_parser('output', help='Get inserted text')
        parser_output.set_defaults(func=self.output)

        parser_exit = subparser.add_parser('exit', help='Exit a rime session')
        parser_exit.set_defaults(func=self.exit_session)

        args = parser.parse_args()
        args.func(args)


class TmuxRimeClient:
    def __init__(self):
        self.server_address = '/tmp/tmux-rime-socket'
        # [test] start session when initializing
        # self.start(0)

    def send_data(self, data, recv=False):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            try:
                s.sendall(data)
                if recv:
                    res = s.recv(1024)
                    return res
            finally:
                s.close()

    def write_pipe(self, data):
        with open(TMUX_RIME_FIFO, 'w') as f:
            f.write(data)

    def start_session(self):
        logging.info('Start session')
        self.send_data('start'.encode('utf-8'))

    def exit_session(self):
        logging.info('Exit session')
        self.send_data('exit'.encode('utf-8'))
        self.write_pipe('exit\n')

    def tmux_insert_text(self):
        inserted_text = self.send_data('output'.encode('utf-8'), True)
        if inserted_text is not None and len(inserted_text) > 0:
            message = 'insert {}'.format(inserted_text.decode('utf-8'))
            logging.info(message)
            self.write_pipe(message + '\n')

    def tmux_update_status(self, status_str):
        if status_str is not None:
            message = 'status {}'.format(status_str.decode('utf-8'))
            logging.info(message)
            self.write_pipe(message + '\n')

    def send_key(self, key, modifier):
        logging.info('Get key: {}, modifier: {}'.format(key, modifier))

        status_str = self.send_data('key {} {}'.format(key, modifier)
                                               .encode('utf-8'), True)

        self.tmux_update_status(status_str)
        self.tmux_insert_text()

    def delete_char(self):
        logging.info('Delete a char')
        status_str = self.send_data('delete'.encode('utf-8'), True)
        self.tmux_update_status(status_str)

    def commit_raw(self):
        logging.info('Commit the raw input')
        status_str = self.send_data('raw'.encode('utf-8'), True)

        self.tmux_update_status(status_str)
        self.tmux_insert_text()

    def output(self):
        res = self.send_data('output'.encode('utf-8'), True)
        if res is not None:
            logging.info(res)


if __name__ == '__main__':
    init_logging()
    client = TmuxRimeClient()
    parser = TmuxRimeParser(client)
    parser.parse()
