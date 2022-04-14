import hashlib
from urllib.request import urlparse

from .get_headers_info import get_headers_info
from .helpers.generate_id import generate_id


def format_headers(hdrs):
	headers = {}
	for header in hdrs:
		header_name = header.lower()
		header_value = hdrs[header]
		headers[header_name] = header_value

	return headers

def get_response_info(response):
	url = response.url
	
	original_url = ""
	
	if response.history:
		original_url = response.history[0].url

	r_url = urlparse(url)
	hostname = r_url.hostname
	port = r_url.port or 0
	protocol = r_url.scheme
	method = response.request.method
	client_http_version = '1.1'
	server_http_version = '1.1'
	code = response.status_code

	req_headers = get_headers_info(response.request.headers, 'REQUEST')
	resp_headers = get_headers_info(response.headers, 'RESPONSE')

	response_id = generate_id()
	response_hash = hashlib.md5(response.content).hexdigest()
	
	#* not saved yet.
	links = response.links

	info = {
	'id':response_id, 'url':url, 'hostname':hostname, 'port':port, 'protocol':protocol, 'method':method,
	'client_http_version':client_http_version, 'server_http_version':server_http_version, 'original_url':original_url,
	'code':code, 'response_hash':response_hash, 'request_headers':req_headers, 'response_headers':resp_headers
	}

	return info

# import requests

# resp = requests.get('https://freebasics.com/', timeout=5)

# info = get_response_info(resp)

# import json

# print( json.dumps(info, indent=2) )