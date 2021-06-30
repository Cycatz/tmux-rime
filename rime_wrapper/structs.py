#!/usr/bin/env python

from ctypes import *

class RimeSchemaListItem(Structure):
    _fields_ = [('schema_id', c_char_p),
                ('name', c_char_p),
                ('reserved', c_void_p)]


class RimeSchemaList(Structure):
    _fields_ = [('size', c_size_t),
                ('list', POINTER(RimeSchemaListItem))]


class RimeCommit(Structure):
    _fields_ = [('data_size', c_int),
                ('text', c_char_p)]

class RimeCandidate(Structure):
    _fields_ = [('text',     c_char_p),
                ('comment',  c_char_p),
                ('reserved', c_void_p)]


class RimeMenu(Structure):
    _fields_ = [('page_size',                   c_int),
                ('page_no',                     c_int),
                ('is_last_page',                c_bool),
                ('highlighted_candidate_index', c_int),
                ('num_candidates',              c_int),
                ('candidates',                  POINTER(RimeCandidate)),
                ('select_keys',                 c_char_p)]
                 
class RimeComposition(Structure):
    _fields_ = [('length',   c_int),
                ('cursor_pos', c_int),
                ('sel_start',  c_int),
                ('sel_end',    c_int),
                ('preedit',    c_char_p)]



class RimeContext(Structure):
    _fields_ = [('data_size',            c_int),
                ('composition',          RimeComposition),
                ('menu',                 RimeMenu),
                # v0.9.2   
                ('commit_text_preview',  c_char_p),
                ('select_labels',        POINTER(c_char_p))]
