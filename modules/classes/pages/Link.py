import posixpath
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .CredStore import CredentialStorage
from .functions import create_url, get_url_info, normalize_path


class ResponseHandler:
	def __init__(self, settings):
		self.settings = settings

class URL:
	def __init__(self, tag=None, attr=None, url=None, value=None):
		self.tag = tag
		self.attr = attr
		self.url = url
		self.value = value

	def __repr__(self):
		return "<Link(tag='%s' attr='%s' url='%s')>"%(self.tag, self.attr, self.url)

	def __str__(self):
		return self.url

class HTMLHandler(ResponseHandler):
	
	def create_absolute_url(self, source_url, url):

		if self.is_special_scheme(url):
			return url

		source_link_info = get_url_info(source_url)
		link_info = get_url_info(url)

		source_scheme = source_link_info.get('protocol')
		source_host = source_link_info.get('host')
		source_path = source_link_info.get('path')

		scheme = link_scheme = link_info.get('protocol')
		host = link_host = link_info.get('host')
		path = link_path = link_info.get('path')

		#transform relative paths into absolute path.
		
		"""
		url could be of this form:
		 	1) http://example.com/path/here
		 	2) //example.com/path/here
		 	3) /path/here
		 	4) here/
		
		if url does not have a scheme, use the source url's scheme as it's scheme.
		if url does not have a host, use the source url's host as it's host.

		"""

		if not scheme and not host:
			#url takes the form of 3) or 4)
			s_path = posixpath.dirname(source_path)
			pp = posixpath.join(s_path, path)
			pp = posixpath.normpath(pp)
			path = pp

		if not scheme:
			#url takes the form of 2) or 3) or 4)
			scheme = source_scheme

		if not host:
			#url takes the form of 3) or 4)
			host = source_host

		params = link_info.get('params')
		query = link_info.get('query')
		fragment = link_info.get('fragment')

		#remove query and fragment.
		# params = ""
		query = ""
		fragment = ""

		url = create_url(scheme=scheme,host=host,path=path,params=params,query=query,fragment=fragment)

		return url

	def is_special_scheme(self, url):

		url = url.lstrip()

		if not ':' in url:
			return False

		url_scheme = url.split(':', 1)[0].strip()

		schemes = ['about','data','javascript', 'mailto', 'tel', 'file', 'irc', 'ws', 'wss']

		if url_scheme.lower() in schemes:
			return True

		#file://, irc://, javascript:, about:, data:, mailto:

	def process_links(self, source_url, links):
		urls = set()
		
		for link in links:
			url = str(link)
			url = self.create_absolute_url(source_url, url)
			urls.add(url)
		
		return urls

	def handle_response(self, response):
		
		source_url = response.url
		content = response.content

		links = []

		b = BeautifulSoup(content, features='html.parser')

		if b:
			pattern = re.compile('.')
			
			href_element = b.findAll(attrs={'href':pattern})
			
			if href_element:
				
				for element in href_element:
					
					link = element.get('href', '').strip()
					
					if not link.startswith('#'):
						link = URL(element.name, 'href', element.get('href'), element.getText())

						links.append(link)

		links = self.process_links(source_url, links)
		return links
	
class XMLHandler(HTMLHandler):
	pass

class Link:
	
	def __init__(self, response, settings={}):
		
		self.settings = settings
		self.response = response

		self.handlers = {
		'text/html':[HTMLHandler(settings)],
		'application/xhtml+xml':[HTMLHandler(settings)],
		'text/xml':[XMLHandler(settings)]
		}

	def get_content_type(self):
		content_type_field = self.response.headers.get('Content-Type', '')
		fields = content_type_field.split('; ')
		return fields[0].strip().lower()

	def get_handler(self, content_type):
		return self.handlers.get(content_type)

	def extract_links(self):
		content_type = self.get_content_type()
		handlers = self.get_handler(content_type)

		if not handlers:
			return []
		
		links = []
		
		for handler in handlers:
			links.extend(handler.handle_response(self.response))
			break

		return links

	def __repr__(self):
		return 'Link <%s>' %(self.response.url)
