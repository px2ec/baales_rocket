
import modcom

class ModDev(object):
	# "Private" variables for instance
	__n_inst = 0 # Instance counter classes

	# "Private" variables for class
	_enabled = False
	_my_id = 0
	_mc = None

	def __init__(self):
		super(ModDev, self).__init__()
		self.__n_inst = 0
		self._my_id = ModDev.__n_inst
		ModDev.__n_inst += 1
		self._enabled = True

	def __del__(self):
		if self._mc:
			del self._mc
		ModDev.__n_inst -= 1
