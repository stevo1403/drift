import json

import gevent
from gevent import socket, time

from .functions import (get_path_info, get_url_info, is_domain_allowed, is_ip,
                        is_ip_allowed)
from .Thread import Bot


class Scraper:

	def __init__(self, controller=None):
		
		self.controller = controller

		#bots instance
		self.bots = []

		#maximum number of bots to create
		self.max_bots_size = 5

		#verbosity > 0 prints error, >=2 prints warning, >=4 prints info, 5 prints a lot of things.
		self.verbosity = 3
		
		#start time.
		self.start_time = 0

		#stop time.
		self.stop_time = 0

		#output file
		self.output = None

		#specify a status code to output file mapping.
		#e.g {404:'404-links.json'} would save urls returning 404 not found to file '404-links.json'
		self.output_files = {}

	def get_info(self):
		info = {}
		info['processed_links'] = self.controller.processed_links
		info['forbidden_links'] = self.controller.forbidden_links
		info['prohibited_links'] = self.controller.prohibited_links
		info['misc_links'] = self.controller.misc_links
		info['unknown_links'] = self.controller.unknown_links
		info['error_links'] = self.controller.error_links

		return info

	def print_exception(self, message):
		if self.verbosity > 0:
			print(message)

	def print_info(self, message):
		if self.verbosity >= 4:
			print(message)

	def resolve_domains(self):
		domains = self.controller.get_program_option('include_domain')

		self.print_info("[+] Resolving allowed %d hostnames into ip address."%(len(domains)))
		self.print_info('')
		for domain in domains:
			try:
				name, alias, address = socket.gethostbyname_ex(domain)
				self.controller.resolved_hosts.update(address)
			except Exception as e:
				self.print_exception("[-] Exception while resolving hostname '%s': %s"%(domain, e))
		self.print_exception('')

	def set_output_file(self, output):
		self.output = output
		return self

	def get_output_file(self):
		return self.output

	def save_json_file(self, content, filename, indent=2):
	
		with open(filename,'wt') as f:
			json.dump(content,f,indent=indent)

		print("[+] %s record(s) saved into file '%s'."%(len(content),filename))
		return filename

	def set_output(self, status_code, filename):

		"""
		@param status_code: the status code or alias 
		@type status_code: int | str
		@param filename: the filename to save all urls that returns `status_code`.
		@type filename: str
		"""

		self.output_files[status_code] = filename

		return self
	def save_output(self):

		if not self.output_files:
			return None

		four_oh_one_file = self.output_files.get(401, self.output_files.get('prohibited_links'))
		four_oh_three_file = self.output_files.get(403, self.output_files.get('forbidden_links'))
		four_oh_four_file = self.output_files.get(404, self.output_files.get('misc_links'))
		three_hundred_file = self.output_files.get(300, self.output_files.get('redirected_links'))
		
		four_hundred_plus_file = self.output_files.get('unknown_links')
		
		five_hundred_file = self.output_files.get(500, self.output_files.get('error_links'))

		processed_file = self.output_files.get(999, self.output_files.get('processed_links'))

		all_file = self.output_files.get(0, self.output_files.get('all_links')) or  self.output_files.get('total_links')

		return_code = 0

		if four_oh_four_file:
			self.save_json_file( list(self.controller.misc_links), four_oh_four_file)
			return_code = 1

		if four_oh_three_file:
			self.save_json_file( list(self.controller.forbidden_links), four_oh_three_file)
			return_code = 1

		if four_oh_one_file:
			self.save_json_file( list(self.controller.prohibited_links), four_oh_one_file)
			return_code = 1

		if all_file:
			self.save_json_file( list(self.controller.total_links), all_file)
			return_code = 1

		if three_hundred_file:
			self.save_json_file( list(self.controller.redirected_links), three_hundred_file)
			return_code = 1

		if four_hundred_plus_file:
			self.save_json_file( list(self.controller.unknown_links), four_hundred_plus_file)
			return_code = 1

		if five_hundred_file:
			self.save_json_file( list(self.controller.error_links), five_hundred_file)
			return_code = 1

		if processed_file:
			self.save_json_file( list(self.controller.processed_links), processed_file)
			return_code = 1

		return return_code

	def start(self):

		self.start_time = time.time()

		self.print_info("[+] Started Link Scraping at %s."%(time.ctime()))
		self.print_info('')

		self.print_info("[+] Starting scraping with %s links."%(len(self.controller.acquired_links)))
		self.print_info("[+] Allowed Hosts: %s."%(', '.join( self.controller.get_program_option('include_host') or [] )))
		self.print_info("[+] Allowed Domains: %s."%(', '.join( self.controller.get_program_option('include_domain') or [] )))
		self.print_info("[+] Allowed Schemes: %s."%(', '.join( self.controller.get_program_option('allowed_protocols') or self.controller.allowed_protocols )))
		self.print_info("[+] Allowed Filetypes: %s."%(', '.join( self.controller.get_program_option('allowed_filetypes') or self.controller.allowed_filetypes )))
		self.print_info("[+] Number of Threads: %s."%(self.max_bots_size))

		#load_urls that would be processed by the bots.
		self.controller.load_urls()
		self.controller.bots_count = self.max_bots_size

		#resolve allowed domains to allowed hosts
		self.resolve_domains()

		for i in range(self.max_bots_size):
			bot = Bot(self.controller)
			bot.setName(str(i))
			bot.verbosity = self.verbosity
			bot.start()
			self.bots.append(bot)

		g_hub = gevent.get_hub()
		g_hub.NOT_ERROR += (KeyboardInterrupt, )

		try:
			gevent.joinall(
				self.bots
			)
		except KeyboardInterrupt as e:
			print(e)
		except Exception as e:
			print('Exception: ', e)
			raise e

		self.stop_time = time.time()
		
		t = self.stop_time - self.start_time

		if self.output:
			print('[+] Saving scraped links into \'%s\'.'%(self.output))
			self.save_json_file(list(self.controller.total_links), self.output)
			print()

		self.save_output()

		active_threads = 0
		for thread in self.controller.threads:
			if thread.isAlive():
				print("[+] Waiting for %s."%(thread.getName()))
				active_threads = 1

		if active_threads:
			print("[+] Done with all threads.")

		self.print_info('')
		self.print_info('[+] Link Scraping took %d second(s).'%(t))
		self.print_info('')