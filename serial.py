#
# micropython-serial - pySerial-like interface for MicroPython
# https://github.com/pfalcon/micropython-serial
#
# Copyright (c) 2014 Paul Sokolovsky
# Licensed under MIT license
#
import os
import termios


class SerialException(OSError):
    pass


class SerialDisconnectException(SerialException):
    pass


class Serial:

    SPEED_MAP = { 9600: termios.B9600, 115200: termios.B115200 }

    def __init__(self, port, speed, timeout=None, **kwargs):
        assert timeout is None, "Only no-timeout mode is supported"
        self.port = port
        self.speed = speed
        self.open()

    def open(self):
        self.fd = os.open(self.port, os.O_RDWR | os.O_NOCTTY)
        termios.setraw(self.fd)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(self.fd)
        #print("tcgetattr result:", iflag, oflag, cflag, lflag, ispeed, ospeed, cc)
        speed = self.SPEED_MAP[self.speed]
        termios.tcsetattr(self.fd, termios.TCSANOW, [iflag, oflag, cflag, lflag, speed, speed, cc])

    def write(self, data):
        return os.write(self.fd, data)

    def read(self, size=1):
        buf = b""
        c = 0
        while size > 0:
            chunk = os.read(self.fd, size)
            l = len(chunk)
            if l == 0:
                # If we read 0 butes, it means that port is gone
                # (for example, underlying hardware like USB adapter
                # disconnected)
                raise SerialDisconnectException("Port disconnected")
            size -= l
            buf += bytes(chunk)
            c += 1

        return buf
