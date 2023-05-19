#!/usr/bin/env python
import os
import re
import sys
import logging
import socketserver
from rime_wrapper import RimeWrapper


def init_logging():
    logging_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    logging_path = os.path.join(logging_dir, 'tmux_rime_server.log')

    file_handler = logging.FileHandler(filename=logging_path)
    stderr_handler = logging.StreamHandler(sys.stderr)
    handlers = [file_handler, stderr_handler]

    logging.basicConfig(format='[%(asctime)s] %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        level=logging.INFO,
                        handlers=handlers)


class TmuxRimeSession:
    def start(self):
        self.rime = RimeWrapper()
        self.rime.start()
        # self.rime.set_schema('bopomofo_tw')
        # self.rime.set_schema('japanese')
        self.rime.set_schema('chemical-kb')
        # self.rime.set_schema('luna_pinyin')
        # print("Schemas:", self.rime.get_schema_list())
        self.output_text = ''

    def finish(self):
        self.rime.finish()

    def handle_key(self, key):
        self.output_text = ''
        # Enter key
        if key == 0xd:
            self.rime.process_key(65293, 0)
        else:
            self.rime.process_key(key, 0)
        self.update_commit_text()
    def delete_char(self):
        self.rime.process_key(65288, 0)

    def update_commit_text(self):
        """ Commit the text """
        commit_text_str = self.rime.get_commit()
        self.output_text = commit_text_str
        # self.clear_state()

    def commit_raw_str(self):
        """ Get the raw input  """
        self.output_text = self.rime.get_input_str()
        self.clear_state()

    def clear_state(self):
        """ Clear the composition """
        self.rime.clear_composition()

    def get_output_text(self):
        return self.output_text

    def get_status_str(self):
        res = ''
        composition_preedit = self.rime.get_composition_preedit()

        if composition_preedit:
            res = '{} | '.format(composition_preedit)
            candidates = self.rime.get_candidates()
            for i, candidate in enumerate(candidates):
                text, comment = candidate
                res += '{}. {} '.format(i + 1 , text)
        return res


class TmuxRimeRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip().decode('utf-8')
        res = None
        if data.startswith('key'):
            res = self.server.handle_key(data)
        elif data.startswith('output'):
            res = self.server.get_output_text()
        elif data.startswith('raw'):
            res = self.server.commit_raw()
        elif data.startswith('delete'):
            res = self.server.delete_char()
        elif data.startswith('exit'):
            logging.info('Exit the session')
            self.server.exit_session()
        else:
            command = data.split(' ')[0]
            logging.warning('Unknown command: {}'.format(command))

        if res is not None:
            logging.info('Send "{}"'.format(res))
            self.request.sendall(res.encode('utf-8'))

class TmuxRimeServer(socketserver.TCPServer):
    def __init__(self):
        # Currently not support multiple sessions
        # self.sessions = {}
        self.session = TmuxRimeSession()
        self.session.start()
        self.server_address = ('127.0.0.1', 2133)
        socketserver.TCPServer.allow_reuse_address = True
        socketserver.TCPServer.__init__(self,
                                        self.server_address,
                                        TmuxRimeRequestHandler)

    def start_server(self):
        self.serve_forever()

    def close_server(self):
        self._BaseServer__shutdown_request = True

    def exit_session(self):
        logging.info('Exit session')
        self.session.finish()
        self.close_server()

    def handle_key(self, data):
        key = int(re.split('\s', data)[1])
        logging.info('Received key: {}' .format(key))
        self.session.handle_key(key)
        return self.session.get_status_str()

    def commit_raw(self):
        logging.info('Commit the raw input')
        self.session.commit_raw_str()

    def delete_char(self):
        logging.info('Delete a char')
        self.session.delete_char()
        return self.session.get_status_str()

    def get_output_text(self):
        text = self.session.get_output_text()
        logging.info('Get output text: {}'.format(text))
        return text


if __name__ == '__main__':
    init_logging()
    with TmuxRimeServer() as server:
        server.start_server()
