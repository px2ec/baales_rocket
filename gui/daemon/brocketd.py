
from PyQt4 import QtCore
import modcom
import moddev
import gmousedev
import sys


import pyautogui
from pymouse import PyMouse

from time import sleep


if sys.platform.startswith('win'):
	import ctypes
	MOUSEEVENTF_MOVE = 0x0001 # mouse move
	MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move
	MOUSEEVENTF_MOVEABS = MOUSEEVENTF_MOVE + MOUSEEVENTF_ABSOLUTE

	MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down 
	MOUSEEVENTF_LEFTUP = 0x0004 # left button up 
	MOUSEEVENTF_RIGHTDOWN = 0x0008
	MOUSEEVENTF_RIGHTUP = 0x0010

ENABLE_INTR = 48

class gMouseD(QtCore.QThread):

	_gmd = None
	Available = False
	Initialized = False
	#ErrorFlag = False # Error flag for any device error

	# _acX_l, _acY_l, _acZ_l = 0, 0, 0
	# _vX_c, _vY_c, _vZ_c = 0, 0, 0
	ToggleEnable = False
	_buttonI_l, _buttonD_l, _buttonTgl_l = 1, 1, 1
	_posX_c, _posY_c = 0, 0
	_posX_l, _posY_l = 0, 0
	SpeedCursor = 255/12
	StepCursor = 1
	DeadZone = 30
	m = PyMouse()

	def __init__(self):
		super(gMouseD, self).__init__()
		pyautogui.FAILSAFE = False 
		pyautogui.MINIMUM_DURATION = 0.00001

	def __del__(self):
		if self._gmd:
			del self._gmd

	def scanDevices(self):
		self._mc = modcom.ModCom(True)
		if not self._mc._assigned:
			del self._mc
			return
		#print "Device found"
		#print "Device description: %s" % self._mc._md
		if self._mc._md == "GLVMOUSE":
			self._gmd = gmousedev.gMouseDev()
			self._gmd._mc = self._mc
			self.Available = True
			return
		if self._mc != None:
			del self._mc
	#ErrorFlag = False # Error flag for any device error
				
	def run(self):
		self._posX_l, self._posY_l = pyautogui.position()
		while self.Available:
			self._refresh()
			# self.ToggleEnable = True
			if self.ToggleEnable:
				lsttmpX, lsttmpY = self._calculate(self.StepCursor, self.SpeedCursor)
				self._clickingmouse()
				self._movingmouse(lsttmpX, lsttmpY, self.StepCursor)
				# self.usleep((1000)/self.StepCursor)
				# sleep((0.001)/self.StepCursor)
			else:
				self._posX_l, self._posY_l = self.m.position()
				# sleep(0.001)

	def _refresh(self):
		self._gmd.getState()
		if self._gmd.buttonTgl != self._buttonTgl_l:
			if self._gmd.buttonTgl == 0:
				self.ToggleEnable = not self.ToggleEnable
				self.emit(QtCore.SIGNAL('toggle()'))
		self._buttonTgl_l = self._gmd.buttonTgl

	def _calculate(self, step, speed):
		return [], []
	# 	self._vX_c, self._vY_c, self._vZ_c = self._acX_l + self._gmd.acX, self._acY_l + self._gmd.acY, self._acZ_l + self._gmd.acZ
	# 	self._acX_l, self._acY_l, self._acZ_l = self._gmd.acX, self._gmd.acY, self._gmd.acZ
	#  	tox, toy = self._vY_c, self._vZ_c
	# 	self._posX_c, self._posY_c = self._gmd.tX/speed + self._posX_l, self._gmd.tY/speed + self._posY_l
	# 	lstposX, lstposY = [], []
	# 	for n in range(step - 1):
	# 		lstposX.append((n + 1)*(self._gmd.tX/(step*speed)))
	# 		lstposY.append((n + 1)*(self._gmd.tY/(step*speed)))
	# 	return lstposX, lstposY
	def _movingmouse(self, lstposX, lstposY, step):
		if not step == 1:
			for n in range(step - 1):
				cx, cy = lstposX[n] + self._posX_l, lstposY[n] + self._posY_l
				pyautogui.moveTo(cx, cy)
				#self.usleep((1000)/step)
				#sleep((0.001)/step)
		if self._gmd.abstX > self.DeadZone:
			self._posX_c = self._gmd.tX/self.SpeedCursor + self._posX_l
		else: 
			self._posX_c = self._posX_l

		yoff = 50
		if self._gmd.tY > self.DeadZone + yoff or self._gmd.tY < -self.DeadZone + yoff:	
			self._posY_c = -(self._gmd.tY - yoff)/self.SpeedCursor + self._posY_l
		else: 
			self._posY_c = self._posY_l
		self.m.move(self._posX_c, self._posY_c)
		# pyautogui.moveTo(self._posX_c, self._posY_c)
		self._posX_l, self._posY_l = self.m.position()
		# self._posX_l, self._posY_l = self._posX_c, self._posY_c

	def _clickingmouse(self):
		if sys.platform.startswith('win'):
			x = 65536L * self._posX_c / ctypes.windll.user32.GetSystemMetrics(0) + 1
			y = 65536L * self._posY_c / ctypes.windll.user32.GetSystemMetrics(1) + 1
			ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVEABS, x, y, 0, 0)

		if self._gmd.buttonI != self._buttonI_l:
			if self._gmd.buttonI == 0 :
				# self.m.press(self._posX_c, self._posY_c, 1)
				if sys.platform.startswith('win'):
					ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
				else:
					pyautogui.mouseDown(button='left')
			else:
				# self.m.release(self._posX_c, self._posY_c, 1)
				if sys.platform.startswith('win'):
					ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
				else:
					pyautogui.mouseUp(button='left')
		if self._gmd.buttonD != self._buttonD_l:
			if self._gmd.buttonD == 0 :
				# self.m.press(self._posX_c, self._posY_c, 3)
				if sys.platform.startswith('win'):
					ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
				else:
					pyautogui.mouseDown(button='right')
			else:
				# self.m.release(self._posX_c, self._posY_c, 3)
				if sys.platform.startswith('win'):
					ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
				else:
					pyautogui.mouseUp(button='right')
		self._buttonI_l, self._buttonD_l = self._gmd.buttonI, self._gmd.buttonD