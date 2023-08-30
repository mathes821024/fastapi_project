# Oracle数据模型
from ctypes import Structure, c_char

class ZmqMessage(Structure):
    _fields_ = [("merNo", c_char * 16),
                ("tranDate", c_char * 9)]
