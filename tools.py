import argparse
import os
import signal

pid_filepath = os.path.join( os.path.dirname(__file__), 'pids.txt')


def get_cmd_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--kill', '-k', action='store_true',dest='kill', help='specify that the server proces should be killed.')
	return parser, parser.parse_args()

if __name__ == '__main__':
	parser, args = get_cmd_args()
	
	kill = args.kill
	
	if kill:
		if os.path.exists(pid_filepath) and os.path.isfile(pid_filepath):
			with open(pid_filepath, 'rt', encoding='utf-8') as f:
				pid = f.read().strip()
				if pid.isnumeric():
					pid = int(pid)
					os.kill(pid, signal.SIGINT)
					print("[+] The server process(pid=%s) was terminated successfully."%(pid))
					
					#erases the file containing the pid.
					open(pid_filepath, 'wt').close()

				else:
					print("[!] The server's PID was not found in the file.")
		else:
			print("[!] The pid file does not exist.")
	else:
		parser.print_help()