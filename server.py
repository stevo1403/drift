import argparse
import importlib
import io
import json
import os
import pydoc
import secrets
import subprocess
import sys
import time
from threading import Thread

from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)

import rpyc
from rpyc.utils.server import ThreadedServer

MAIN_DIR = os.path.dirname(__file__)

config_filename = "server.conf"

config_filepath = os.path.join( os.path.dirname(__file__), config_filename)

pid_filepath = os.path.join( os.path.dirname(__file__), 'pids.txt')

verbosity = 5

def read_stdout(process, stream):

	stdout = process.stdout
	print('enter read_stdout')
	while True:
		print('read_stdout loop')

		if process.poll() != None:
			print('BROKEN: Process is DEAD.')
			break

		print('after polling.')

		available_bytes = len(stdout.peek())

		print('after peeking.')
		if not available_bytes or available_bytes <= 0:
			# print('BROKEN: NO BYTES TO READ..')
			# break
			continue

		output = stdout.read(available_bytes)

		print('after reading.')
		print(output)

		if output:
			stream.write(output)
			print('after writing.')
		else:
			print('BROKEN: NO OUTPUT.')
			break

		print('STREAM: ', stream.getvalue())
		print('STREAM: ', stream.getvalue())

def get_config():
	try:
		with open(config_filepath, mode='rt', encoding='utf-8') as cfg:
			return json.load(cfg)
	except Exception as e:
		print("[-] An Error occurred while loading configuration: ", e)
		return {}

def import_modules():
	
	"""
	Import modules from the 'modules' directories.
	Only files(modules) that ends with .py, .pyo, .pyd are imported.

	"""

	_module_directory = 'modules'
	
	print("[+] Importing modules from directory '%s'."%(_module_directory))
	print()

	modules_directory = os.path.join(MAIN_DIR, _module_directory)

	MODULES_STORE = {}

	if not os.path.exists(modules_directory):
		print("[-] Cannot find the module directory '%s'."%(_module_directory))
	else:
		directory_objects = os.listdir(modules_directory)

		modules = []
		
		allowed_extensions = ['.py', '.pyo', '.pyd']

		config = importlib.import_module("%s.%s"%(_module_directory, 'config'))

		DISABLED_MODULES = []

		if 'DISABLED_MODULES' in dir(config):
			DISABLED_MODULES = config.__dict__['DISABLED_MODULES']

		if 'BEFORE_LOADING' in dir(config):
			BEFORE_LOADING = config.__dict__['BEFORE_LOADING']

		if 'Loaders' in dir(config):
			loaders = config.Loaders()

			print("[+] %s loader(s) would be run before loading modules."%( len(BEFORE_LOADING) ) )

			for loader in BEFORE_LOADING:
				print("[+] Calling loader '%s'."%(loader))
				loaders.call_loader(loader)

			print()

		for directory_object in directory_objects:

			file = os.path.join(modules_directory, directory_object)

			if os.path.isfile(file):

				filename, extension = os.path.splitext( os.path.basename(file) )

				if extension.lower() in allowed_extensions:
					print("[+] Found module '%s'."%(filename))
					modules.append(file)

		print()
		print("[+] Found %s modules in modules directory."%(len(modules)))

		loaded_modules = 0

		for module in modules:

			filename, extension = os.path.splitext( os.path.basename(module) )
			
			if filename in DISABLED_MODULES:
				continue

			module_name = '%s.%s'%(_module_directory, filename)

			print("[+] Importing module '%s' from module directory '%s'."%( os.path.basename(module), _module_directory) )
			
			m = importlib.import_module(module_name)

			MODULES_STORE[filename.lower()] = m

			loaded_modules += 1

		print()
		print("[+] Loaded %s modules."%(loaded_modules))
		print()

	return MODULES_STORE

def write_to_pid_file():
	with open(pid_filepath, 'wt') as f:
		f.write( str(os.getpid()) + "\n")

def clear_pid_file():
	with open(pid_filepath, 'wt') as f:
		f.close()

class StdoutThread(Thread):
	def __init__(self, *args, **kwargs):
		self.stream = None
		self.process = None
		
		self.stopped = False

		super().__init__(*args, **kwargs)

	def get_stream(self):
		return self.stream

	def run(self):
		if self.stream != None and self.process != None:
			read_stdout(self.process, self.stream)
		
		self.stopped = True

class ProcessSpawnerService(rpyc.Service):
	
	def __init__(self, *args, **kwargs):
		
		self.processes = {}
		self.processes_info = {}
		self.threads = {}
		
		self.config = get_config()
		self.modules = import_modules()

		super().__init__(*args, **kwargs)

	def on_connect(self, conn):
		print("Connection: ", conn)
		super().on_connect(conn)

	def exposed_start_process(self, args):
		print("START_PROCESS: ", args)
		p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE,)
		
		job_id = secrets.token_hex()

		self.processes[job_id] = p
		self.processes_info[job_id] = args

		return job_id

	def exposed_end_process(self, job_id):
		print("END_PROCESS: ", job_id)

		if job_id in self.processes.keys():
			return self.processes[job_id].kill()
		else:
			return -1

	def exposed_get_stdout(self, job_id, timeout=1):
		
		if self.exposed_get_status(job_id) != "ALIVE":
			return b""

		print("GET_STDOUT: ", job_id)

		if self.threads.get(job_id) != None:
			t = self.threads.get(job_id)
		else:
			p = self.processes[job_id]
			stream = io.BytesIO()

			t = StdoutThread()
			
			t.stream = stream
			t.process = p

			t.daemon = True
			t.start()

			self.threads[job_id] = t

		stream = t.get_stream()

		t1 = time.time()
		t2 = t1 + timeout

		while True:
			t = time.time()
			if t >= t2:
				break

		output = stream.getvalue()
		
		print(self.config)

		store_stdout = self.config.get('STORE_STDOUT_STREAM')
		max_stdout_bff_size = self.config.get('MAX_STDOUT_BUFFER_SIZE')

		"""
		bff = ABCDEF
		max_stdout = 2
		bff = EF
		"""

		# stream.seek(0)
		# stream.truncate()

		if store_stdout:
			if max_stdout_bff_size > 0:
				if len(output) > max_stdout_bff_size:
					print('clearing buffer 1')
					output = output[-max_stdout_bff_size:]
					stream.seek(0)
					stream.truncate()
					stream.write(output)
		else:
			stream.seek(0)
			stream.truncate()
			print('clearing buffer 2')

		return output

	def exposed_get_stderr(self, job_id):
		pass

	def test_access(self):
		pass

	def exposed_run_module(self, module_name, attribute=None, **options):

		if not module_name:
			ret_message = "[+] %d modules were loaded.\r\n\r\n"%(len(self.modules))
			for module in self.modules.keys():
				ret_message += "[+] Found module '%s'.\r\n"%(module)

			return ret_message

		else:
			module_name = module_name.lower()

		if module_name in self.modules.keys():
			module = self.modules.get(module_name)
			
			if attribute:
				try:
					_object = module.__getattribute__(attribute)
				except AttributeError:
					return "[-] Module '%s' does not have attribute '%s'."%(module_name, attribute)
			else:
				_object = module			
			
			if options:
				return _object(**options)
			else:
				return pydoc.render_doc( _object, renderer=pydoc.plaintext )
		else:
			return "[-] Error module '%s' does not exist."%(module_name)

	def exposed_say_hello(self, greetings):
		return "HELLO"

	def exposed_get_status(self, job_id):
		p = self.processes[job_id]
		return "ALIVE" if p.poll() == None else "DEAD"

	def exposed_send_stdin(self, job_id, data, newline=None):
		print("SEND_STDIN: ", job_id)

		p = self.processes[job_id]
		
		if hasattr(data, 'encode'):
			data = data.encode()

		if newline == True:
			data += b"\r\n"

		if p.poll() == None:
			p.stdin.write(data)
			p.stdin.flush()

		return 1

	def exposed_get_output(self, job_id):
		pass

	def exposed_cancel_jobs(self, job_ids=[]):
		job_ids = job_ids or self.processes.keys()

		job_ids = list(job_ids)

		for job_id in job_ids:
			process = self.processes.get(job_id, None)

			if process != None:
				process.kill()
				del self.processes[job_id]
			
			if job_id in self.threads:
				del self.threads[job_id]
		
		return 1

	def exposed_cancel_job(self, job_id):
		process = self.processes.get(job_id, None)
		
		print(self.threads, job_id)

		if process != None:
			process.kill()
			
			del self.processes[job_id]
		
		if job_id in self.threads:
			del self.threads[job_id]

			return 1

	def exposed_get_ids(self):
		return list(self.processes.keys())

	def get_job_info(self, job_id):
		return self.processes_info.get(job_id, [])

if __name__ == "__main__":

	config = get_config()

	if not "LISTEN_ADDR" in config.keys():
		hostname = "localhost"
		print("[*] Listen address is not configured, '%s' would be used."%(hostname))
	else:
		hostname = config.get("LISTEN_ADDR")

	if not "LISTEN_PORT" in config.keys():
		port = 18861
		print("[*] Listen port is not configured, port %s would be used."%(port))
	else:
		port = config.get("LISTEN_PORT")

	try:
		write_to_pid_file()
		t = ThreadedServer(ProcessSpawnerService(), port=port, hostname=hostname, protocol_config={'allow_public_attrs':True})
		print("[+] Started the server on %s:%s"%(hostname, port))
		print()
		t.start()
	except Exception as e:
		print("[-] An error occurred: ", e)
	except KeyboardInterrupt:
		print("[-] Exiting the server")
	finally:
		clear_pid_file()