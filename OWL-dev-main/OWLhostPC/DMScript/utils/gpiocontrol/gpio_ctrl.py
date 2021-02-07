"""
Interface to CP210x GPIO Control on Hermes EVT Board
Author  : Madhur Jain <Madhur.Jain@Sandisk.com>
Date    : 05/04/2016
"""
import win32file
import win32con
import ctypes
import os
import sys

CP210x_SUCCESS               	= 0x00
CP210x_DEVICE_NOT_FOUND      	= 0xFF
CP210x_INVALID_HANDLE        	= 0x01
CP210x_INVALID_PARAMETER     	= 0x02
CP210x_DEVICE_IO_FAILED      	= 0x03
CP210x_FUNCTION_NOT_SUPPORTED	= 0x04
CP210x_GLOBAL_DATA_ERROR     	= 0x05
CP210x_FILE_ERROR            	= 0x06
CP210x_COMMAND_FAILED        	= 0x08
CP210x_INVALID_ACCESS_TYPE   	= 0x09

CP210x_GPIO_0 					= 0x0001
CP210x_GPIO_1 					= 0x0002
CP210x_GPIO_2 					= 0x0004
CP210x_GPIO_3 					= 0x0008

class GPIOCtrl(object):	
	def __init__(self, com_port):
		self.com_port = com_port
		is_64bits = sys.maxsize > 2**32
		lib_path = os.path.dirname(os.path.abspath(__file__)) + '\\lib\\'
		lib_path += 'x64' if is_64bits else 'x86'
		self.cp210x = ctypes.windll.LoadLibrary(lib_path + '\\CP210xRuntime.dll')
		
	def ReadIO(self):
		device_handle = win32file.CreateFile(self.com_port,
			win32con.GENERIC_READ|win32con.GENERIC_WRITE,
			0,
			None,
			win32con.OPEN_EXISTING,
			win32con.FILE_ATTRIBUTE_NORMAL|win32con.FILE_FLAG_OVERLAPPED,
			None)
		handle = ctypes.c_int(device_handle)
		reg_latch = ctypes.c_int(0)

		status = self.cp210x.CP210xRT_ReadLatch(handle, ctypes.byref(reg_latch))
		if status != CP210x_SUCCESS:
			print 'Error Reading IO: {}'.format(status)
			return
		win32file.CloseHandle(device_handle)
		return reg_latch.value
		
	def WriteIO(self, mask, value):	
		device_handle = win32file.CreateFile(self.com_port,
			win32con.GENERIC_READ|win32con.GENERIC_WRITE,
			0,
			None,
			win32con.OPEN_EXISTING,
			win32con.FILE_ATTRIBUTE_NORMAL|win32con.FILE_FLAG_OVERLAPPED,
			None)
		handle = ctypes.c_int(device_handle)
		status = self.cp210x.CP210xRT_WriteLatch(handle, mask, value)
		if status != CP210x_SUCCESS:
			print 'Error Writing IO: {}'.format(status)
			return
		win32file.CloseHandle(device_handle)
		
	def TurnOnPwr(self):
		self.WriteIO(CP210x_GPIO_2, 4)
		
	def TurnOffPwr(self):
		self.WriteIO(CP210x_GPIO_2, 0)
		
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print 'Usage: python gpio_ctrl.py <com_port> <pwron|pwroff|readgpio>'
		exit(0)

	com_port = sys.argv[1]
	gpio = GPIOCtrl('\\.\\{}'.format(com_port))
	if sys.argv[2] == 'pwron':
		gpio.TurnOnPwr()
		print 'Powered On'
	elif sys.argv[2] == 'pwroff':
		gpio.TurnOffPwr()
		print 'Powered Off'
	elif sys.argv[2] == 'readgpio':
		print gpio.ReadIO()