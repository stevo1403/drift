import os
import string
from urllib.parse import urlparse

from .functions import create_url, get_url_info, normalize_path


class LinksParser:
	
	def __init__(self, links):
		
		self.links = links
		self.processed_links = set()

	def parse_links(self):

		for link in self.links:
			source_link_url = link.get_source_link()
			link_url = link.get_link_url()
			url = self.create_absolute_url(source_link_url, link_url)
			self.processed_links.add(url)

		return self.processed_links

	def create_absolute_url(self, source_link, link):

		source_link_info = get_url_info(source_link)
		link_info = get_url_info(link)

		source_scheme = source_link_info.get('protocol')
		source_host = source_link_info.get('host')
		source_path = source_link_info.get('path')

		scheme = link_scheme = link_info.get('protocol')
		host = link_host = link_info.get('host')
		path = link_path = link_info.get('path')

		#transform relative paths into absolute path.
		if not link_host and not link_scheme:
			if not path.startswith('/'):
				source_path = os.path.dirname(source_path)
				path = normalize_path(source_path, link_path)

		if not link_scheme:
			scheme = source_scheme

		if not link_host:
			host = source_host

		params = source_link_info.get('params')
		query = source_link_info.get('query')
		fragment = source_link_info.get('fragment')

		url = create_url(scheme=scheme,host=host,path=path,params=params,query=query,fragment=fragment)

		return url

	def is_special_scheme(self,link,strict=True):

		link = link.lstrip()
		l_scheme = urlparse(link).scheme

		schemes = ['about','data','javascript']
		
		if l_scheme + ':' in schemes:
			return True
		else:
			return False
	