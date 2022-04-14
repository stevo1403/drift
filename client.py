import argparse
import importlib
import json
import os
import sys
import time

import rpyc

MAIN_DIR = os.path.dirname(__file__)
config_filename = "server.conf"
config_filepath = os.path.join( os.path.dirname(__file__), config_filename)

def get_cmd_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--module', dest='module', help='specify the module to be called')
	parser.add_argument('-a', '--attribute', dest='attribute', help='specify the attribute to be called in the module.')
	parser.add_argument('-l', '--list-modules',action='store_true', dest='list_modules', help='specify that modules should be listed.')
	parser.add_argument('-o', '--option', action='append', default=[], dest='option', help='specify the keywords argument for the functions.')
	parser.add_argument('-p', '--prettify', action='store_true', dest='prettify', help='specify that the results should be prettified.')

	return parser, parser.parse_args()

def get_config():
	try:
		with open(config_filepath, mode='rt', encoding='utf-8') as cfg:
			return json.load(cfg)
	except Exception as e:
		print("[-] An Error occurred while loading the configuration file: ", e)
		return {}

def parse_options(parser, args):
	options = {}

	for opt in args.option:
		if '=' in opt:
			opt, value = opt.split('=', 1)
			opt = opt.strip()
			options[opt] = value
	
	return options

if __name__ == '__main__':
	
	config = get_config()
	
	port = config.get('LISTEN_PORT', 18861)
	addr = config.get('LISTEN_ADDR', 'localhost')

	c = None

	try:
		c = rpyc.connect(addr, port)
		print("[+] Connected successfully to RPC server on %s:%s."%(addr, port))
	except Exception as e:
		print("[!] Could not connect to the server on the host %s listening on the port %s due to: %s"%(addr, port, e))
		exit(1)

	print()

	parser, args = get_cmd_args()
	attribute = args.attribute
	options = parse_options(parser, args)
	prettify = args.prettify

	if args.list_modules:
		module_name = None
	else:
		module_name = args.module

	result = c.root.run_module(module_name, attribute, **options)

	if prettify and result.__class__ in (dict, list, tuple):
		try:
			print( json.dumps(result), indent=2)
		except Exception as e:
			print(result)
	else:
		print(result)

# c.root.cancel_jobs()

# args =  ['python', 't2.py']

# j_id = c.root.start_process(args)

# print(c.root.get_stdout(j_id).decode())

# c.root.send_stdin(j_id, "Yin Yang", True)

# print(c.root.get_stdout(j_id).decode())

# c.root.send_stdin(j_id, "John Doe", True)

# print(c.root.get_stdout(j_id).decode())

# c.root.cancel_job(j_id)

# time.sleep(3)