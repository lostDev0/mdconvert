from enum import IntEnum, Enum

class auto_number(IntEnum):
    _count = 0
    def __new__(cls):
        value = _count
        _count += 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

class block(auto_number):
    INVALID = ()
    BOLD = ()
    ITALIC = ()
    MONOSPACE = ()
    SECTION = ()