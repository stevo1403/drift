
class BaseHandler:
	def __init__(self, settings):
		self.settings = settings

class HTMLHandler(BaseHandler):
	
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
	
class XMLHandler(BaseHandler):
	pass

class ResponseHandler:
	
	def __init__(self, response, handlers={}, settings={}):
		
		self.settings = settings
		self.response = response

		self.handlers = {
		# 'text/html':[HTMLHandler(settings)],
		# 'application/xhtml+xml':[HTMLHandler(settings)],
		# 'application/xhtml':[HTMLHandler(settings)],
		# 'text/xml':[XMLHandler(settings)]
		}

		self.handlers.update(handlers)

	def get_content_type(self):
		content_type_field = self.response.headers.get('Content-Type', '')
		fields = content_type_field.split('; ')
		return fields[0].strip().lower()

	def get_handlers(self, content_type):
		return self.handlers.get(content_type)

	def process(self):
		content_type = self.get_content_type()
		handlers = self.get_handlers(content_type) or []

		result = {}

		for handler in handlers:

			if type(handler) is type(object):
				# handler is a class.
				handler_instance = handler(self.settings)
				r = handler_instance.handle_response(self.response)
			else:
				# handler is an instance.
				r = handler.handle_response(self.response)
				
			if result.get(content_type):
				result[content_type].append(r)
			else:
				result[content_type] = [r]

		return result