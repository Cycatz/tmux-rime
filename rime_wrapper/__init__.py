# -*- coding: utf-8 -*-

from ctypes import *
from rime_wrapper.raw import *


class RimeWrapper:
    def __init__(self):
        self.rime_wrapper_ptr = rime_wrapper_init()

    def start(self):
        rime_wrapper_start(self.rime_wrapper_ptr, 0)

    def get_schema_list(self):
        _schema_list = rime_wrapper_get_schema_list(self.rime_wrapper_ptr)

        list_size = _schema_list.contents.size
        schema_list = _schema_list.contents.list

        items = []
        for i in range(list_size):
            schema = schema_list[i]
            items.append((schema.schema_id.decode('utf-8'),
                          schema.name.decode('utf-8')))
        rime_wrapper_free_schema_list(self.rime_wrapper_ptr, _schema_list)
        return items

    def set_schema(self, schema_id):
        return rime_wrapper_set_schema(self.rime_wrapper_ptr, c_char_p(schema_id.encode('utf-8')))

    def get_context(self):
        _context = rime_wrapper_get_context(self.rime_wrapper_ptr)
        rime_wrapper_free_context(self.rime_wrapper_ptr, _context)

    def process_key(self, keycode, mask):
        return rime_wrapper_process_key(self.rime_wrapper_ptr, keycode, mask)

    def get_input_str(self):
       _input_str = rime_wrapper_get_input_str(self.rime_wrapper_ptr)
       input_str = cast(_input_str, c_char_p).value.decode('utf-8')
       rime_wrapper_free_str(_input_str)
       return input_str

    def finish(self):
        rime_wrapper_finish(self.rime_wrapper_ptr)


# rime_wrapper.start()
# rime_wrapper.finish()
