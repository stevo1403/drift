import argparse
import importlib
import io
import json
import os
import subprocess
import sys

import rpyc

MAIN_DIR = os.path.dirname(__file__)
config_filename = "server.conf"
config_filepath = os.path.join( os.path.dirname(__file__), config_filename)

def find_server():

	config = get_config()
	
	port = config.get('LISTEN_PORT', 18861)
	addr = config.get('LISTEN_ADDR', 'localhost')

	print("[+] Checking if the server is up.")
	print()
	print("[+] Hostname => %s"%(addr))
	print("[+] Port => %s"%(port))
	print()

	server_status = 0

	for i in range(2):
		try:
			c = rpyc.connect(addr, port)
			server_status = 1
			break
		except Exception as e:
			print("[!] Could not connect to the server on the host %s listening on the port %s."%(addr, port))
			if i == 0:
				print("[+] Trying again...")
			else:
				print("[-] Quitting!")

	return (addr, port) if server_status else ()

def get_config():
	try:
		with open(config_filepath, mode='rt', encoding='utf-8') as cfg:
			return json.load(cfg)
	except Exception as e:
		print("[-] An Error occurred while loading the configuration file: ", e)
		return {}

if __name__ == '__main__':
	server_status = find_server()

	if not server_status:
		
		print()
		print("[+] Creating a new server process.")
		
		server_script = os.path.join(MAIN_DIR, os.path.dirname(__file__), 'server.py')
		for index, python_executable in enumerate(['python3', 'python', 'python'+str(sys.version_info.major)]):
			try:
				args = [python_executable, server_script]
				p = subprocess.Popen(args, stdout=subprocess.PIPE)
				print("[+] The server has successfully been launched(pid=%s)."%(p.pid))
				break
			except Exception as e:
				if index == 2:
					print("[-] Could not launch the server due to the following error: %s"%(e))
		
	else:
		print("[+] The server is up and running on %s:%s."%(server_status))
