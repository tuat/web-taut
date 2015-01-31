# coding: utf-8

import os
import sys
import signal

class Watcher:
    def __init__(self):
        self.child = os.fork()

        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            print('\nExit...')
            self.kill()

        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass
