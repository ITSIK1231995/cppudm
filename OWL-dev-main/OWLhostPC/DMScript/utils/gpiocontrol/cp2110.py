"""
Python interface for CP2110
Author  : Akshay Naik <Akshay.Naik@Sandisk.com>
Date    : 08/05/2018
"""
import ctypes
import os
import sys
import numpy as np
import time

VID = 0x10c4
PID = 0xea80

ERROR_CODES = {
    0x0 : 'HID_UART_SUCCESS',
    0x1 : 'HID_UART_DEVICE_NOT_FOUND',
    0x2 : 'HID_UART_INVALID_HANDLE',
    0x3 : 'HID_UART_INVALID_DEVICE_OBJECT',
    0x4 : 'HID_UART_INVALID_PARAMETER',
    0x5 : 'HID_UART_INVALID_REQUEST_LENGTH',
    0x10 : 'HID_UART_READ_ERROR',
    0x11 : 'HID_UART_WRITE_ERROR',
    0x12 : 'HID_UART_READ_TIMED_OUT',
    0x13 : 'HID_UART_WRITE_TIMED_OUT',
    0x14 : 'HID_UART_DEVICE_IO_FAILED',
    0x15 : 'HID_UART_DEVICE_ACCESS_ERROR',
    0x16 : 'HID_UART_DEVICE_NOT_SUPPORTED',
    0xff : 'HID_UART_UNKNOWN_ERROR'
}

PIN_CONFIG = {
    'HID_UART_GPIO_MODE_INPUT' : 0x0,
    'HID_UART_GPIO_MODE_OD' : 0x1,
    'HID_UART_GPIO_MODE_PP' : 0x2,
    'HID_UART_GPIO_MODE_FUNCTION1' : 0x3
}

PIN_INDEX = {
    0 : 0,
    1 : 1,
    2 : 2,
    3 : 3,
    4 : 6,
    5 : 7,
    6 : 10,
    7 : 11,
    8 : 12,
    9 : 13
}
class CP2110Error(Exception):
    """Exception Class for Pico Logger exceptions"""
    def __init__(self, message):
        super(CP2110Error, self).__init__(message)
        self.message = 'CP2110Error: ' + message

    def __str__(self):
        return repr(self.message)

class CP2110(object):
    '''CP2110 Class'''
    handle = ctypes.c_void_p(0)
    def __init__(self):
        '''Initialize'''
        is_64bits = sys.maxsize > 2**32
        arch = 'x64' if is_64bits else 'x86'
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(file_path, 'lib', arch))
        dll_file = os.path.join(file_path, 'lib', arch, 'SLABHIDtoUART.dll')

        self.dll = ctypes.windll.LoadLibrary(dll_file)
        num_devices = ctypes.c_ushort(0)
        c_vid = ctypes.c_ushort(VID)
        c_pid = ctypes.c_ushort(PID)
        ret = self.dll.HidUart_GetNumDevices(ctypes.byref(num_devices), c_vid, c_pid)
        # Open Device
        ret = self.dll.HidUart_Open(ctypes.byref(self.handle), 0, c_vid, c_pid)
        if ret != 0:
            raise CP2110Error('__init__ failed! : HidUart_Open : {}'.format(ERROR_CODES[ret]))

    def clear_gpio(self, pin):
        mask = 1 << PIN_INDEX[pin]
        latch &= ~mask
        ret = self.dll.HidUart_WriteLatch(self.handle, ctypes.c_ulong(latch), ctypes.c_ulong(mask))
        if ret != 0:
            raise CP2110Error('clear_gpio failed! : HidUart_WriteLatch : {}'.format(ERROR_CODES[ret]))

    def set_gpio(self, pin):
        mask = 1 << PIN_INDEX[pin]
        latch |= mask
        ret = self.dll.HidUart_WriteLatch(self.handle, ctypes.c_ulong(latch), ctypes.c_ulong(mask))
        if ret != 0:
            raise CP2110Error('set_gpio failed! : HidUart_WriteLatch : {}'.format(ERROR_CODES[ret]))

    def read_latch(self):
        latch = ctypes.c_uint(0)
        ret = self.dll.HidUart_ReadLatch(self.handle, ctypes.byref(latch))
        if ret != 0:
            raise CP2110Error('read_latch failed! : HidUart_ReadLatch : {}'.format(ERROR_CODES[ret]))
        return latch.value

    def powercycle(self):
        # Power OFF : clear pin2
        mask = 1 << PIN_INDEX[2]
        ret = self.dll.HidUart_WriteLatch(self.handle, ctypes.c_ulong(0), ctypes.c_ulong(mask))
        if ret != 0:
            raise CP2110Error('powercycle failed! : HidUart_WriteLatch : {}'.format(ERROR_CODES[ret]))
        time.sleep(2)

        # Power ON : set pin2 and 5
        mask |= 1<< PIN_INDEX[5]
        print(bin(mask))
        ret = self.dll.HidUart_WriteLatch(self.handle, ctypes.c_ulong(mask), ctypes.c_ulong(mask))
        if ret != 0:
            raise CP2110Error('powercycle failed! : HidUart_WriteLatch : {}'.format(ERROR_CODES[ret]))


    def close(self):
        '''Close method'''
        ret = self.dll.HidUart_Close(self.handle)
        if ret != 0:
            raise CP2110Error('read_latch failed! : HidUart_Close : {}'.format(ERROR_CODES[ret]))

def main():
    '''main function'''
    try:
        # Initialize
        dev = CP2110()
        dev.powercycle()
        dev.close()

    except (CP2110Error, OSError) as error:
        print(error)
        exit(0)

if __name__ == '__main__':
    main()
