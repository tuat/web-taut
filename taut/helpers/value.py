# coding: utf-8

def force_integer(value, default=1):
    try:
        return int(value)
    except:
        return default
