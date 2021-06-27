#!/usr/bin/env python
import rime_wrapper
from ctypes import *


rime = rime_wrapper.RimeWrapper()
rime.start()
rime.get_context()
rime.get_input_str()
print(rime.get_schema_list())
rime.finish()

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
