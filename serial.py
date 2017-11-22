#
# micropython-serial - pySerial-like interface for MicroPython
# https://github.com/pfalcon/micropython-serial
#
# Copyright (c) 2014 Paul Sokolovsky
# Licensed under MIT license
#
import os
import termios
import ustruct
import fcntl
import uselect

FIONREAD = const(0x541b)

class SerialException(OSError):
    pass


class SerialDisconnectException(SerialException):
    pass


class Serial:

    BAUD_MAP = {
        9600: termios.B9600,
        # From Linux asm-generic/termbits.h
        19200: 14,
        57600: termios.B57600,
        115200: termios.B115200
    }

    def __init__(self, port, baudrate, timeout=None, **kwargs):
        self.port = port
        self.baudrate = baudrate
        self.timeout = -1 if timeout is None else timeout * 1000
        self.open()

    def open(self):
        self.fd = os.open(self.port, os.O_RDWR | os.O_NOCTTY)
        termios.setraw(self.fd)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(self.fd)
        #print("tcgetattr result:", iflag, oflag, cflag, lflag, ispeed, ospeed, cc)
        baudrate = self.BAUD_MAP[self.baudrate]
        termios.tcsetattr(self.fd, termios.TCSANOW, [iflag, oflag, cflag, lflag, baudrate, baudrate, cc])
        self.poller = uselect.poll()
        self.poller.register(self.fd, uselect.POLLIN | uselect.POLLHUP)

    def close(self):
        os.close(self.fd)

    def inWaiting(self):
        buf = ustruct.pack('I', 0)
        fcntl.ioctl(self.fd, FIONREAD, buf, True)
        return ustruct.unpack('I', buf)[0]

    def write(self, data):
        return os.write(self.fd, data)

    def read(self, size=1):
        buf = b""
        c = 0
        while size > 0:
            if not self.poller.poll(self.timeout):
                break
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
