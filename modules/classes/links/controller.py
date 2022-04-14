from threading import Event, Lock

import requests

from .functions import (get_path_info, get_url_info, is_domain_allowed, is_ip,
                        is_ip_allowed)
from .Link import Link
from .LinkParser import LinksParser


class Controller:
	def __init__(self):

		#keeps the thread status.
		self.thread_status = {}
		
		#flag that tells the threads to stop.
		self.stop_operation = Event()

		#flag that tells the other threads to wait.
		self.pause_operation = Event()

		#thread lock
		self.lock = Lock()

		#holds all the threads created.
		self.threads = []
		
		self.total_links = set()

		#contains all processed links.
		self.processed_links = set()

		# 200 OK links.
		self.ok_links = set()

		#extracted links that have not been processed.
		self.acquired_links = set()

		#401 unauthorized links.
		self.prohibited_links = set()

		#403 forbidden links
		self.forbidden_links = set()

		#404 not found links 
		self.misc_links = set()

		#unknown links
		self.unknown_links = set()

		#redirected links
		self.redirected_links = set()

		#external links
		self.external_links = set()

		#error links
		self.error_links = set()
		
		#thread status
		self.threads_status = {}

		#maximum queue size
		self.queue_size = 10

		#allowed domains
		self.allowed_hosts = []
		# self.allowed_hosts = ['127.0.0.1:8080','localhost:8080']

		#allowed_filetypes
		self.allowed_filetypes = ['html', 'jsp', 'jspx', 'xhtml', 'asp', 'aspx', 'php']

		#allowed protocols
		self.allowed_protocols = ['http', 'https']

		self.filetypes = set()

		self.current_path = '/'

		#thread lock
		self.lock = Lock()

		self.thread_status = {}

		self.queue_length = 10

		self.queue_size = 10

		#specify the number of threads
		self.threads_count = 5

		#specify the seconds for request to timeout
		self.request_timeout = 5

		#maximum response size in kilobytes(kb)
		self.max_response_size = 102401

		#maximum number of redirect
		self.max_redirects = 5

		#timeout for http(s) requests
		self.request_timeout = 10

		#http request headers
		self.request_headers = {}

		#path prefix
		self.path_prefix = []

		#http(s) request settings
		self.request_settings = {}

		#program options.
		self.program_settings = {}

		#url file
		self.url_file = None

		#url file handle
		self.url_file_handle = None

		#callable that accepts one argument(the number of urls to load) and returns a list of urls.
		self.url_loader = None

		#list of urls
		self.urls = set()

		#events
		self.threads_event = {}

		#the state of each thread.
		self.thread_state = {}
		
		#list of allowed_content_types
		self.allowed_content_types = ['text/html', 'text/xhtml']
		
		#resolved hosts
		self.resolved_hosts = set()

		#include domains
		self.include_domains = set()

		#source page to links mapping.
		self.link_mapping = {}

	def is_host_allowed(self, url_host):

		include_domain = self.get_program_option('include_domain') or []
		exclude_domain = self.get_program_option('exclude_domain') or []
		
		include_host = self.get_program_option('include_host') or []
		exclude_host = self.get_program_option('exclude_domain') or []

		allow_subdomain = self.get_program_option('match_subdomain')

		matched_host = False
		
		include_host.extend(self.resolved_hosts)
		include_domain.extend(self.include_domains)

		if is_ip(url_host):
			matched_host = True
			if not is_ip_allowed(url_host,include_host,exclude_host):
				return False
		
		if not matched_host:
			if not is_domain_allowed(url_host,include_domain,exclude_domain, allow_subdomain):
				return False
		return True

	def is_scheme_allowed(self, url_scheme):
		allowed_schemes = self.get_program_option('allowed_protocols') or self.allowed_protocols
		if not url_scheme in allowed_schemes:
			return False
		else:
			return True

	def is_extension_allowed(self, url_ext):
		allowed_ext = self.get_program_option('include_filetype') or self.allowed_filetypes
		disallowed_ext = self.get_program_option('exclude_filetype') or []

		if not url_ext == '':
			if url_ext in disallowed_ext or not url_ext in allowed_ext:
				return False
		return True
	
	def is_directory_allowed(self, url_path):
		#directories that are not allowed.
		disallowed_directories = self.get_program_option('exclude_directories') or []

		if url_path in disallowed_directories:
			return False
		
		for p in disallowed_directories:
			if p.startswith('*') and p.endswith('*'):
				_p = p.strip('*')
				if _p in url_path:
					return False
			if p.startswith('*'):
				_p = p.lstrip('*')
				if url_path.endswith(_p):
					return False
			if p.endswith('*'):
				_p = p.rstrip('*')
				if url_path.startswith(_p):
					return False
		return True

	def is_prefix_allowed(self, url_path):

		include_path_prefix = self.get_program_option('include_path_prefix') or []
		exclude_path_prefix = self.get_program_option('exclude_path_prefix') or []

		for prefix in exclude_path_prefix:
			if url_path.startswith(prefix):
				if prefix == url_path:
					return False
				elif len(url_path) > len(prefix):
					if prefix.endswith('/'):
						return False

		if include_path_prefix:
			matched = False
			for prefix in include_path_prefix:
				if url_path.startswith(prefix):
					if prefix == url_path:
						matched = True
					elif len(url_path) > len(prefix):
						if prefix.endswith('/'):
							matched = True
				if matched:
					break
			
			#prefix list exists but the url path does not match any.
			if not matched:
				return False
		return True

	def is_url_allowed(self, url):
		"""
		Returns a boolean which indicates whether a link should be processed or not.
		@param url: the url to perform a check on
		@type url: str
		@rtype: bool
		"""
		
		url_info = get_url_info(url)
		
		url_scheme = url_info.get('protocol')

		url_host = url_info.get('host')
		
		url_path = url_info.get('path')
		
		url_path_info = get_path_info(url_path)

		url_ext = url_path_info.get('extension').strip('.')

		url_path = url_path_info.get('path')
		
		
		if not self.is_scheme_allowed(url_scheme):
			return False

		if not self.is_extension_allowed(url_ext):
			return False

		if not self.is_directory_allowed(url_path):
			return False

		if not self.is_prefix_allowed(url_path):
			return False

		if not self.is_host_allowed(url_host):
			return False

		return True

	def handle_redirects(self,response):
		"""
		Handle redirects for each.
		@param response: response object
		@type response: requests.models.Response
		@rtype: requests.models.Response
		"""
		sentry = 0
		
		while True:
			
			if response.status_code == 302:
				redirect_url = response.headers.get('Location')
				if redirect_url:
					pass

			sentry += 1
			if sentry >= self.max_redirects:
				break
		
		return response
	
	def set_program_option(self,opt,val):
		"""
		Creates or Updates the program option named `opt` and set its value to `val`.
		@param opt: the name of the option to set
		@type opt: str
		@param val: the value of the option `opt`
		@type val: string or list or set
		@rtype: str or list or set
		"""
		self.program_settings[opt] = val
		return self

	def get_program_option(self,opt):
		"""
		Returns the value of the program option `opt`.
		@param opt: the name of the option to set
		@type opt: str
		@rtype: str or list or set
		"""
		return self.program_settings.get(opt)

	def set_request_option(self,opt,val):
		"""
		Creates or Updates the request option named `opt` and set its value to `val`.
		@param opt: the name of the option to set
		@type opt: str
		@param val: the value of the option `opt`
		@type val: string or list or set
		@rtype: str or list or set
		"""
		self.request_settings[opt] = val
		return self

	def get_request_option(self,opt):
		"""
		Returns the value of the request option `opt`.
		@param opt: the name of the option to set
		@type opt: str
		@rtype: str or list or set
		"""
		return self.request_settings.get(opt)

	def get_request_options(self):
		"""
		Returns a dictionary containing the request settings.
		@rtype dict
		"""
		return self.request_settings

	def get_request_timeout(self):
		return self.request_timeout

	def store_links(self, links):
		allowed_links = set()

		for link in links:
			if self.is_url_allowed(link):
				allowed_links.add(link)
			else:
				self.external_links.add(link)
		
		self.acquired_links.update(allowed_links)
		self.total_links.update(allowed_links)

		return allowed_links

	def create_session(self):

		#creates a session.
		session = requests.Session()
		
		raw_cookies = ""
		
		cookies = self.get_request_option('cookies') or ''
		
		if cookies:

			for cookie in cookies:
				
				cookie_name = cookie
				cookie_value = cookies[cookie_name]
				
				c = "%s=%s; "%(cookie_name,cookie_value)
				
				raw_cookies += c

		if raw_cookies:
			session.headers.update({'Cookie':raw_cookies})

		return session

	def add_header(self, header, value):
		self.request_headers[header] = value
		return self

	def update_headers(self, headers):
		self.request_headers.update(headers)
		return self

	def get_request_headers(self):
		return self.request_headers

	def register_event(self, thread_id, event):
		if thread_id in self.threads_event:
			self.threads_event[thread_id].add(event)
		else:
			self.threads_event[thread_id] = set([event])

		return self

	def delete_event(self, thread_id, event):
		if thread_id in self.threads_event:
			if event in self.threads_event[thread_id]:
				self.threads_event[thread_id].remove(event)
		return self

	def has_event(self, thread_id, event):
		if thread_id in self.threads_event:
			if event in self.threads_event[thread_id]:
				return True

		return False

	def get_event_ids(self, event):
		
		"""
		Return the ids of threads that has registered `event`.
		"""

		event_ids = []
		for thread_id in self.threads_event:
			if event in self.threads_event[thread_id]:
				event_ids.append(thread_id)

		return event_ids

	def get_thread_state(self, thread_id):
		return self.thread_state.get(thread_id)

	def set_thread_state(self, thread_id, state):
		self.thread_state[thread_id] = state
		return self

	def get_bots_size(self):
		return len(self.thread_state)

	def process_response(self, response):

		print(response)
		
		#add the url to list of processed links.
		self.processed_links.add(response.url)

		if response.status_code < 300:
			link = Link(response)
			links = link.extract_links()
			
			for link in links:
				if response.url in self.link_mapping:
					self.link_mapping.add(link)
				else:
					self.link_mapping = set([link])

				if not link in self.processed_links:
					#this has been 'encountered' but not processed.
					self.processed_links.add(link)
					print('[+] Got url \'%s\' from page \'%s\'.'%(link, response.url))
					
					if self.is_url_allowed(link):
						self.acquired_links.add(link)

		elif 300 >= response.status_code < 400:
			self.redirected_links.add(response.url)

		elif response.status_code == 401:
			self.prohibited_links.add(response.url)
		
		elif response.status_code == 403:
			self.forbidden_links.add(response.url)
		
		elif response.status_code == 404:
			self.misc_links.add(response.url)

		elif response.status_code >= 500:
			self.error_links.add(response.url)
		else:
			self.unknown_links.add(response.url)

		if response.history:
			for entry in response.history:
				try:
					self.processed_links.add(entry.url)
				except Exception as e:
					print('[-] Exception while adding urls from history: ', e)

		#remove the url from acquired_links.
		self.remove_link(response.url)

	def remove_link(self, link):
		
		"""
		Remove `link` from acquired links.
		@param link: the link(url) to remove
		@type link: str
		@rtype bool
		"""
		try:
			if link in self.acquired_links:
				self.acquired_links.remove(link)
				return True
		except Exception as e:
			print('Exception occurred while removing link.')

		return False
	
	def is_task_done(self):
		"""
		Returns True if all threads have exited, otherwise False.
		@rtype: bool
		"""
		for value in self.thread_status.values():
			if value == 1:
				return False
		return True
	
	def get_lock(self):
		return self.lock

	def add_url(self, url):
		self.acquired_links.add(url)

	def add_urls(self, urls):
		allowed_domains = self.get_program_option('include_domain') or []
		allowed_domains = allowed_domains.copy()
		allowed_domains.extend(self.include_domains)

		domains = set()
		
		for url in urls:
			host = get_url_info(url).get('host')
			if host and not host in allowed_domains:
				domains.add(host)
		
		self.include_domains.update(domains)
		self.acquired_links.update(urls)

	def load_urls_from_handle(self, handle, size=10):
		urls = set()
		for line in handle:
			line = line.strip()
			if line:
				urls.add(line)

			if len(urls) == size:
				break
		return urls

	def open_file(self, filename, mode='rt'):
		handle = open(filename, mode, encoding='utf-8')
		return handle

	def load_urls(self, size=10):

		if len(self.acquired_links) >= size:
			return self.acquired_links

		if self.url_file:
			if not self.url_file_handle:
				self.url_file_handle = self.open_file(self.url_file)
			urls = self.load_urls_from_handle(self.url_file_handle, size)
			self.acquired_links.update(urls)

		if len(self.acquired_links) >= size:
			return self.acquired_links

		if self.urls:
			while self.urls:
				self.acquired_links.add(self.urls.pop(0))
				if len(self.acquired_links) >= size:
					break

		if len(self.acquired_links) >= size:
			return self.acquired_links

		if self.url_loader:
			self.acquired_links.update(self.url_loader(size))
		
		return self.acquired_links

	def get_urls(self, size=10):
		
		with self.lock:
			if not self.acquired_links:
				self.load_urls(size=size)

			urls = set()

			if self.acquired_links:
				while self.acquired_links:
					urls.add(self.acquired_links.pop())
					if len(urls) >= 10:
						break

			return list(urls)
