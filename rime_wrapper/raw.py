#!/usr/bin/env python
import os
import platform
from ctypes import *
import ctypes.util

import rime_wrapper
from rime_wrapper.structs import *

system = platform.system()

if system == 'Windows':
    library_name = 'libwrime.dll'
elif system == 'Darwin':
    library_name = 'libwrime.dylib'
else:
    library_name = 'libwrime.so'

filename = os.path.join(os.path.dirname(rime_wrapper.__file__), library_name)

try:
    _lib = ctypes.CDLL(filename)
except (OSError, TypeError):
    _lib = None
    raise RuntimeError('Rime wrapper library not found')

rime_wrapper_init = _lib.rime_wrapper_init
rime_wrapper_init.argtypes = []
rime_wrapper_init.restype = c_void_p

rime_wrapper_start = _lib.rime_wrapper_start
rime_wrapper_start.argtypes = [c_void_p, c_int]
rime_wrapper_start.restype = c_int

rime_wrapper_finish = _lib.rime_wrapper_finish
rime_wrapper_finish.argtypes = [c_void_p]
rime_wrapper_finish.restype = c_int


rime_wrapper_get_input_str = _lib.rime_wrapper_get_input_str
rime_wrapper_get_input_str.argtypes = [c_void_p]
rime_wrapper_get_input_str.restype = c_void_p

rime_wrapper_free_str = _lib.rime_wrapper_free_str
rime_wrapper_free_str.argtypes = [c_void_p]
rime_wrapper_free_str.restype = None

rime_wrapper_set_cursor_pos = _lib.rime_wrapper_set_cursor_pos
rime_wrapper_set_cursor_pos.argtypes = [c_void_p, c_int]
rime_wrapper_set_cursor_pos.restype = None

rime_wrapper_clear_composition = _lib.rime_wrapper_clear_composition
rime_wrapper_clear_composition.argtypes = [c_void_p]
rime_wrapper_clear_composition.restype = None

rime_wrapper_get_commit = _lib.rime_wrapper_get_commit
rime_wrapper_get_commit.argtypes = [c_void_p]
rime_wrapper_get_commit.restype = POINTER(RimeCommit)

rime_wrapper_free_commit = _lib.rime_wrapper_free_commit
rime_wrapper_free_commit.argtypes = [c_void_p, POINTER(RimeCommit)]
rime_wrapper_free_commit.restype = None

rime_wrapper_get_context = _lib.rime_wrapper_get_context
rime_wrapper_get_context.argtypes = [c_void_p]
rime_wrapper_get_context.restype = POINTER(RimeContext)

rime_wrapper_free_context = _lib.rime_wrapper_free_context
rime_wrapper_free_context.argtypes = [c_void_p, POINTER(RimeContext)]
rime_wrapper_free_context.restype = None

rime_wrapper_get_schema_list = _lib.rime_wrapper_get_schema_list
rime_wrapper_get_schema_list.argtypes = [c_void_p]
rime_wrapper_get_schema_list.restype = POINTER(RimeSchemaList)

rime_wrapper_free_schema_list = _lib.rime_wrapper_free_schema_list
rime_wrapper_free_schema_list.argtypes = [c_void_p, POINTER(RimeSchemaList)]
rime_wrapper_free_schema_list.restype = None

rime_wrapper_process_key = _lib.rime_wrapper_process_key
rime_wrapper_process_key.argtypes = [c_void_p, c_int, c_int]
rime_wrapper_process_key.restype = c_int
