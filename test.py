#!/usr/bin/env python
from rime_wrapper import RimeWrapper
from ctypes import *

class TmuxRimeSession:
    def __init__(self):
        self.rime = RimeWrapper()
        self.rime.start()
        self.rime.set_schema('bopomofo')
        self.output_text = ''

    def __del__(self):
        self.rime.finish()

    def handle_key(self, key):
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

    def display_status_str(self):
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
        print('Current output: ', self.output_text)
        print(self.display_status_str())

class TmuxRimeServer:
    def __init__(self):
        self.sessions = {}

    def send_command(self, sid, command):
        session = self.sessions.get(sid)
        if session is None:
            self.sessions[sid] = self.TmuxRimeSession()
        self.sessions[sid].send_input(key, mask)

session = TmuxRimeSession()

session.print_info()

session.handle_key('j')
session.handle_key('i')
session.handle_key('3')
session.print_info()
session.handle_key('Space')
session.print_info()

session.handle_key('j')
session.handle_key('i')
session.handle_key('3')

session.print_info()

session.handle_key('Space')
session.print_info()


session.handle_key('Space')
session.print_info()


session.handle_key('j')
session.handle_key('i')
session.handle_key('3')
session.print_info()


session.handle_key('Space')
session.print_info()

session.handle_key('j')
session.handle_key('i')
session.handle_key('3')
session.print_info()


session.handle_key('Return')
session.print_info()




# print(rime.get_menu())
# print(rime.get_composition())
# print(rime.get_commit_text_preview())
# print('Commit: ', rime.get_commit())
# print(rime.get_context())
# print('Input string: ', rime.get_input_str())
# print('Schema list: ', rime.get_schema_list())
# rime.finish()

# a = c_int(3)
# print(type(POINTER(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
# print(rime_wrapper.test(byref(a)))
