#!/usr/bin/env python
import os
import re
import logging
import socketserver
from rime_wrapper import RimeWrapper


class TmuxRimeSession:
    def __init__(self):
        self.start()

    def __del__(self):
        self.finish()

    def start(self):
        self.rime = RimeWrapper()
        self.rime.start()
        self.rime.set_schema('bopomofo')
        self.output_text = ''

    def finish(self):
        self.rime.finish()

    def handle_key(self, key, modifier):
        self.output_text = ''
        if key == 'Return':
            self.commit_raw_str()
        elif key == 'Del':
            pass
        elif key == 'Space':
            if not self.rime.has_candidates():
                self.commit_text()
            else:
               self.rime.process_key(ord(' '), 0)
        else:
            self.rime.process_key(ord(key), 0)

    def commit_text(self):
        """ Commit the text """
        commit_text_str = self.rime.get_commit_text_preview()
        self.output_text = commit_text_str
        self.clear_state()

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

    def print_info(self):
        print('=============================')
        print('Current output: ', self.get_output_text())
        print(self.get_status_str())


class TmuxRimeRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.login_string = 'Hello guest!\r\n'
        self.exit = False

    def handle(self):
        while not self.exit:
            data = self.request.recv(1024).strip().decode('utf-8')
            if data.startswith('start '):
                self.server.start_session(data)
            elif data.startswith('key '):
                message = self.server.handle_key(data)
                self.request.sendall(message.encode('utf-8'))
            elif data.startswith('exit '):
                self.server.exit_session(data)
            else:
                command = data.split(' ')[0]
                logging.warning('Unknown command: {}'.format(command))

                
class TmuxRimeServer(socketserver.UnixStreamServer):
    def __init__(self):
        self.sessions = {}
        self.server_address = '/tmp/tmux-rime.rime'
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        socketserver.UnixStreamServer.__init__(self,
                                               self.server_address,
                                               TmuxRimeRequestHandler)

    def start_server(self):
        server.serve_forever()

    def start_session(self, data):
        session_id = int(re.split('\s', data)[1])
        if self.sessions.get(session_id) is not None:
            logging.warning('Session {} exists!'.format(session_id))
        else:
            self.sessions[session_id] = TmuxRimeSession()
            print('Start session {}'.format(session_id))

    def exit_session(self, data):
        session_id = int(re.split('\s', data)[1])
        session = self.sessions.get(session_id)
        if session is None:
            logging.warning('Session {} does not exist!'.format(session_id))
        else:
            session.finish()
            print('Exit session {}'.format(session_id))

    def handle_key(self, data):
        session_id, key, modifier = tuple(re.split('\s', data)[1:])
        session_id = int(session_id)
        session = self.sessions.get(session_id)

        if session is None:
            logging.warning('Session {} does not exist!'.format(session_id))
            # output the error message
            pass
        else:
            session.handle_key(key, modifier)
            return session.get_status_str()

if __name__ == '__main__':
    server = TmuxRimeServer()
    server.start_server()
