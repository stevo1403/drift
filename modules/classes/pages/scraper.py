import argparse
import json
import os
import string
import time
from urllib.parse import urlparse

from controller import Controller
from Link import Link
from LinkParser import LinksParser
from ScrapeIt import Scraper
from Thread import Bot

from functions import is_domain, is_ip, is_subdomain


def get_cmd_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', '-u', action='append', default=[], metavar='URL1,URL2,..', help='specify the url(s) to fetch links from (e.g "http://example.com,http://example2.com).', dest='url')
	parser.add_argument('--url-list', '-L', metavar='URLS_FILE', help='specify the file containing url(s).', dest='url_list')
	parser.add_argument('--cookie','-c',action='append',default=[],help='send cookie along with request(COOKIE_NAME=COOKIE_VALUE).',dest='cookie')
	parser.add_argument('--raw-cookie','-b',default=None,help='send raw cookie along with each request.',dest='raw_cookie')
	parser.add_argument('--header',action='append',default=[],help='specify the request headers.',dest='headers')
	parser.add_argument('--include-prefix', '-P', action='append', default=[], metavar='DIRECTORY_PREFIX1,DIRECTORY_PREFIX2,..', help='specify that only the url whose path begins with one of the specified prefix should be processed.', dest='include_prefix')
	parser.add_argument('--exclude-prefix', action='append', default=[], metavar='DIRECTORY_PREFIX1,DIRECTORY_PREFIX2,..', help='specify that urls whose path begins with one of the specified prefix should be not processed.', dest='exclude_prefix')
	parser.add_argument('--directories', '-I', action='append', default=[], metavar='DIRECTORY1,DIRECTORY2,..', help='specify that the specified path(s) should be the starting point for link scraping.', dest='include_directory')
	parser.add_argument('--exclude-directories', '-X', action='append', default=[], metavar='DIRECTORY1,DIRECTORY2,..', help='specify that urls whose path matches one of the specified path should not be processed.', dest='exclude_directory')
	parser.add_argument('--domain', '-D', action='append', default=[], metavar='DOMAIN1,DOMAIN2,..', help='specify that only urls whose domain name matches one of the specified domain(s) should  be processed.', dest='include_domain')
	parser.add_argument('--exclude-domain', action='append', default=[], metavar='DOMAIN1,DOMAIN2,..', help='specify that urls whose domain name matches one of the specified domain(s) should not be processed.', dest='exclude_domain')
	parser.add_argument('--accept-filetype', '-A', action='append', default=[], metavar='FILETYPE1,FILETYPE2,..', help='specify that only the url whose filetype matches one of the specified filetypes be processed.', dest='include_filetype')
	parser.add_argument('--reject-filetype', '-R', action='append', default=[], metavar='FILETYPE1,FILETYPE2,..', help='specify that urls whose filetype matches one of the specified filetypes should not be processed.', dest='exclude_filetype')
	parser.add_argument('--host', '-H', action='append', default=[], metavar='HOST1,HOST2,..', help='specify that only the url whose host matches one of the specified host(s) be processed(Unspecified hosts are not processed).', dest='include_host')
	parser.add_argument('--exclude-host', action='append', default=[], metavar='HOST1,HOST2,..', help='specify that urls whose host matches one of the specified host(s) should not be processed.', dest='exclude_host')
	parser.add_argument('--scheme', '-S', action='append', default=[], metavar='URL_SCHEME1,URL_SCHEME2,..', help='specify that only the url whose scheme matches one of the specified schemes be processed.', dest='scheme')
	parser.add_argument('--timeout', '-T', default=15, type=int, help='specify the timeout for each request (default 15).', dest='timeout')
	parser.add_argument('--verbose', '-v', action='count', default=0, help='specify the verbosity level of the program (default 0).', dest='verbosity')
	parser.add_argument('--directory', '-d', help='specify the directory to save the links file.', dest='directory')
	parser.add_argument('--threads','-t',default=20, type=int, help='number of threads(s) to use (default 20).',dest='thread')
	parser.add_argument('--match-port', action='store_false', help='specify that ports should be matched.', dest='match_port')
	parser.add_argument('--match-subdomain', action='store_false', help='specify that subdomains should be matched', dest='match_subdomain')
	parser.add_argument('--whitelist-url-host', '-W', action='store_true', help='specify that host(s) and domain(s) found in supplied url(s) should be automatically whitelisted', dest='whitelist_url_host')
	parser.add_argument('--save', '-s', action='store_true', help='specify that the links should be saved into a file with a filename format links-<url>.json.', dest='save')
	parser.add_argument('--output', '-o', help='specify the file to write the  links into.', dest='output')
	args = parser.parse_args()
	return (args,parser)

def get_urls_from_file(filename):
	urls = []
	with open(filename,'rt') as f:
		for line in f:
			line = line.strip()
			if line and not line in urls:
				urls.append(line)

	return urls

def get_url_info(url):
	url = url.lstrip()
	parsed_url = urlparse(url)
	info = {
	'host':parsed_url.netloc,'protocol':parsed_url.scheme,
	'query':parsed_url.query,'params':parsed_url.params,
	'fragment':parsed_url.fragment,'path':parsed_url.path
	}
	return info

def sanitize_filename(filename, _allowed_chars=''):
	allowed_chars = string.ascii_letters + string.digits + '-' + '_' + _allowed_chars
	_filename = ""
	for char in filename:
		if not char in allowed_chars:
			if _filename[-1:] == "_":
				char = ""
			else:
				char = "_"

		_filename += char

	return _filename.strip('_')

def save_json_file(content,filename,indent=2):
	
	with open(filename,'wt') as f:
		json.dump(content,f,indent=indent)
	print("[+] %s record(s) saved into file '%s'."%(len(content),filename))
	return filename

def print_time_info():
	month = time.strftime('%B')

	day = time.strftime('%d')

	year = time.strftime('%Y')

	hour = time.strftime('%I')

	minute = time.strftime('%M')

	second = time.strftime('%S')

	meridiem = time.strftime('%p')

	print()

	print("Scraping started on %s %s %s, %s:%s:%s %s."%(month,day,year,hour,minute,second,meridiem))

	print()

def get_paths(urls,with_query=False):
	for url in urls:
		parsed_url = urlparse(url)
		path = parsed_url.path
		query = parsed_url.query
		if with_query:
			if not path:
				path = '/'
			if query:
				path += '?' + query
		
		yield path

def get_headers(args):
	header_fields = {}
	_header_fields = {}
	if args.headers:
		header = args.headers
		for d in header:
			if d:
				r=d.split('=',1)
				k = r[0]
				if len(r) == 1:
					v = ''
				else:
					v=r[1]
				header_fields[k] = v

	for key in header_fields.keys():
		_key = ""
		capitalize = False
		for index,char in enumerate(key):
			if index == 0:
				char = char.upper()
			if capitalize and char.isalpha():
				char = char.upper()
				capitalize = False
			if char == "-":
				capitalize = True
			_key += char
		_header_fields[_key] = header_fields[key]
	header_fields = _header_fields
	return header_fields

def get_list(iterables,sep=[',',' '],unique=True):
	items = []
	for item in iterables:
		processed = False
		for s in sep:
			if s in item:
				_item = item.split(s)
				for i in _item:
					if unique == False or not i in items:
						items.append(i)
				processed = True
				break
		if not processed and not item in items:
			items.append(item)

	return items

def get_path_prefix(args):
	include_prefix = get_list(args.include_prefix)
	exclude_prefix = get_list(args.exclude_prefix)

	for prefix in exclude_prefix:
		if prefix in include_prefix:
			include_prefix.remove(prefix)

	return include_prefix, exclude_prefix

def get_directories(args):
	include_directories = get_list(args.include_directory)
	exclude_directories = get_list(args.exclude_directory)

	for directory in exclude_directories:
		if directory in include_directories:
			include_directories.remove(directory)

	return include_directories, exclude_directories

def get_hosts(args):
	include_host = get_list(args.include_host)
	exclude_host = get_list(args.exclude_host)
	for host in exclude_host:
		if host in include_host:
			include_host.remove(host)

	return include_host, exclude_host
 
def get_filetype(args):
	include_filetype = [f.strip('.') for f in get_list(args.include_filetype)]
	exclude_filetype = [f.strip('.') for f in get_list(args.exclude_filetype)]
	for filetype in exclude_filetype:
		if filetype in include_filetype:
			include_filetype.remove(filetype)

	return include_filetype, exclude_filetype
 
def get_domain(args):
	exclude_domain = get_list(args.exclude_domain)
	include_domain = get_list(args.include_domain)
	for domain in exclude_domain:
		if domain in include_domain:
			include_domain.remove(domain)

	return include_domain, exclude_domain
 
def is_domain_allowed(domain,accept,reject,allow_subdomain=True):
	"""
	Checks if a domain is allowed or not.
	@param domain: the domain to check
	@type domain: str
	@param accept: the list of allowed domains
	@type accept: list
	@param reject: the list of unallowed domains
	@type reject: list
	@param allow_subdomain: allow wildcards in accept or reject list
	@type allow_subdomain: int ;
	@rtype: bool

	"""

	if domain.strip('.') in reject:
		return False

	for d in reject:

		if d.startswith('*') and not allow_subdomain:

			if is_subdomain(domain,d.lstrip('*.')):
				return False

		elif d.startswith('*'):
			d = d.lstrip('*.')
		
		if d == domain:
			return False

	for d in accept:
		if d.startswith('*') and not allow_subdomain:
			if is_subdomain(domain,d.lstrip('*.')):
				return True

		elif d.startswith('*'):
			d = d.lstrip('*.')

		if d == domain:
			return True

	return False

def is_host_allowed(host,accept,reject):
	if host in reject:
		return False
	elif host in accept:
		return True
	else:
		return False

def form_urls(hosts,paths,protocol='http'):
	"""
	Returns a list of urls resulting from mergin each path to each host.
	@param hosts: a list containing hosts.
	@type hosts: list
	@param paths: a list containing paths.
	@type paths: list
	@param protocol: the protocol or scheme of the url
	@type protocol: str
	@rtype list
	"""
	urls = []
	for host in hosts:
		for path in paths:
			url = protocol + '://' + host + path
			urls.append(url)

	return urls

def get_hosts_from_urls(urls,default_scheme='http'):
	hosts = []
	for url in urls:
		
		url_info = get_url_info(url)
		url_scheme = url_info['protocol']
		
		if not url_scheme:
			url = default_scheme + '://' + url 
			url_info = get_url_info(url)
		
		url_domain = url_info['host']
		if url_domain and not url_domain in hosts:
			hosts.append(url_domain)
	
	return hosts

def get_fields(fields):
	_fields = {}
	if fields:
		for d in fields:
			if d:
				r=d.split('=',1)
				k = r[0]
				if len(r) == 1:
					v = ''
				else:
					v=r[1]
				_fields[k] = v
	return _fields

def get_cookies(args):
	cookies = {}
	_cookies = {}
	if args.cookie:
		cookies = get_fields(args.cookie)

	for cookie in cookies:
		_cookies[cookie] = cookies[cookie] + '; '
	cookies = _cookies
	
	return cookies

def get_raw_cookies(args):
	cookies = {}
	raw_cookies = args.raw_cookie
	if not raw_cookies:
		return cookies

	raw_cookies = raw_cookies.split(';')
	for cookie in raw_cookies:
		cookie_component = cookie.split('=',1)
		if len(cookie_component) == 2:
			cookie_name,cookie_value = cookie_component
			cookies[cookie_name.lstrip()] = cookie_value
	
	return cookies

if __name__ == '__main__':
	args, parser = get_cmd_args()
	
	_urls = args.url
	url_file = args.url_list
	
	timeout = args.timeout
	verbose = args.verbosity
	should_save = args.save
	directory = args.directory
	threads_count = args.thread
	match_subdomain = args.match_subdomain
	match_port = args.match_port
	whitelist_url_host = args.whitelist_url_host
	output = args.output

	cookie = args.cookie

	cookies = get_cookies(args)

	raw_cookies = get_raw_cookies(args)

	raw_cookies.update(cookies)

	cookies = raw_cookies

	schemes = args.scheme
	
	include_host = args.include_host
	exclude_host = args.exclude_host
	
	include_directories = args.include_directory
	exclude_directories = args.exclude_directory
	
	include_domain = args.include_domain
	exclude_domain = args.exclude_domain

	include_filetype = args.include_filetype
	exclude_filetype = args.exclude_filetype

	schemes = get_list(schemes)

	include_path_prefix, exclude_path_prefix = get_path_prefix(args)

	include_directories, exclude_directories = get_directories(args)

	include_host, exclude_host = get_hosts(args)

	include_domain, exclude_domain = get_domain(args)

	include_filetype, exclude_filetype = get_filetype(args)

	headers = get_headers(args)
	
	urls = []

	if not _urls and not url_file:
		parser.error("either of the following arguments are required: --url, --url-list/-L")
	
	if _urls:
		urls.extend(_urls)

	if url_file:
		file_urls = get_urls_from_file(url_file)
		urls.extend(file_urls)
	
	if not urls:
		print("[-] No url provided.")

	_urls_ = form_urls(get_hosts_from_urls(urls),include_directories)

	for u in _urls_:
		if not u in urls:
			urls.append(u)

	_urls = []

	allowed_hosts = include_host

	supported_schemes = ['http','https']

	for s in schemes:
		s = s.rstrip('://')
		if s not in supported_schemes:
			raise Exception("Specified scheme '%s' is not supported."%(s))
	
	allowed_filetypes = ['html','xhtml','jsp','jspx','php','asp','aspx']

	if schemes:
		allowed_protocols = schemes
	else:
		allowed_protocols = supported_schemes

	default_scheme = 'http'

	for filetype in allowed_filetypes[::]:
		filetype = filetype.strip()
		if filetype in include_filetype or filetype in exclude_filetype:
			allowed_filetypes.remove(filetype)

	allowed_filetypes.extend(include_filetype)

	if not allowed_filetypes:
		print("[-] No filetype allowed, only paths without filetype would be processed.")

	asked = False
	should_include = False

	for url in urls:
		url_info = get_url_info(url)
		url_scheme = url_info['protocol']
		
		if not url_scheme:
			url = default_scheme + '://' + url
			url_info = get_url_info(url)
		
		url_scheme = url_info['protocol']
		url_domain = url_info['host']

		if url_scheme not in supported_schemes:
			raise Exception("URL '%s' has scheme '%s' which is not supported."%(url,url_scheme))

		if not whitelist_url_host and (include_domain or include_host):
			domain_whitelisted = url_domain in include_domain and not url_domain in include_host and not should_include
			
			if not asked and not domain_whitelisted:
				should_include = input("[*] Do you want to whitelist host(s) and domain(s) found in the supplied urls?(Y)es or (N)o: ").lower()
				print()
				
				if should_include.count('y') or should_include.count('t'):
					should_include = True
				else:
					print("[-] Use the 'whitelist-url-host/-W' flag to enable automatic whitelisting of host(s) found in the url.")
					print()
				asked = True
			
			if not domain_whitelisted:
				print("[-] URL '%s' will not be parsed because its host '%s' is not whitelisted."%(url,url_domain))
				continue
			elif not should_include and (url_domain in exclude_domain or url_domain in exclude_host):
				print("[-] URL '%s' will not be parsed because its host '%s' is not allowed."%(url,url_domain))
				continue

		if is_domain(url_domain) and not url_domain in include_domain:
			include_domain.append(url_domain)
		
		elif is_ip(url_domain) and not url_domain in include_host:
			include_host.append(url_domain)
		else:
			if not url_domain in include_domain:
				include_domain.append(url_domain)

		if not url in _urls:
			_urls.append(url)

	urls = _urls

	links = urls

	if should_save and not output:
		output = sanitize_filename(urls[0])
	
	if output and directory:
		output = os.path.join(directory,output)

	if output and not output.endswith('.json'):
		output += '.json'

	print_time_info()

	print("[+] Starting scraping with %s links."%(len(links)))
	print("[+] Allowed Hosts: %s."%(', '.join(include_host)))
	print("[+] Allowed Domains: %s."%(', '.join(include_domain)))
	print("[+] Allowed Schemes: %s."%(', '.join(allowed_protocols)))
	print("[+] Allowed Filetypes: %s."%(', '.join(allowed_filetypes)))
	print("[+] Number of Threads: %s."%(threads_count))
	print()
	
	t1 = time.time()

	controller = Controller()
	
	controller.allowed_filetypes.extend(allowed_filetypes)

	controller.allowed_hosts = allowed_hosts

	controller.allowed_protocols = allowed_protocols
	
	controller.request_timeout = timeout

	controller.request_headers = headers

	controller.set_request_option('cookies',cookies)

	controller.set_program_option('verbosity',verbose)
	controller.set_program_option('match_subdomain',match_subdomain)

	controller.set_program_option('exclude_directories',exclude_directories)
	
	controller.set_program_option('allowed_protocols',allowed_protocols)
	
	controller.set_program_option('include_path_prefix',include_path_prefix)
	controller.set_program_option('exclude_path_prefix',exclude_path_prefix)

	controller.set_program_option('include_domain',include_domain)
	controller.set_program_option('exclude_domain',exclude_domain)

	controller.set_program_option('include_host',include_host)
	controller.set_program_option('exclude_host',exclude_host)

	controller.set_program_option('include_filetype',include_filetype)
	controller.set_program_option('exclude_filetype',exclude_filetype)
	
	controller.add_urls(urls)

	scraper = Scraper()
	scraper.controller = controller
	scraper.start()