DISABLED_MODULES = [
	#Don't remove this.
	'config',
	'get_server_cert',
	'test',
	'store',
]

BEFORE_LOADING = [
	'load_gevent',
]

class LoaderNotExists(Exception):
	pass

class Loaders:

	"""
	Add custom methods that are to be called before loading the modules in the modules directory. 
	"""

	def load_gevent(self):
		from gevent import monkey as curious_george
		curious_george.patch_all(thread=False, select=False)

	"""
	Leave the methods below alone.
	"""

	def call_loader(self, loader_name):

		if hasattr(self, loader_name):
			return self.__getattribute__(loader_name)()
		else:
			raise LoaderNotExists("Loader '%s' was not registered."%(loader_name))