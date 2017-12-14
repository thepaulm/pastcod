#!/usr/bin/env python

# File for shared code used across source files

import threading

from threading import Lock

# print function with locks for multithreading
def locked_print(*args, **keyword_args):
    lock = Lock()

    lock.acquire()
    if(len(keyword_args) == 0):
        print(" ".join(map(str, args)))
    else:
        print(" ".join(map(str, args)), keyword_args)
    lock.release()

