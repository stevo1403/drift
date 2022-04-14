import hashlib

from .helpers.generate_id import generate_id


def format_headers(hdrs):
	headers = {}
	for header in hdrs:
		header_name = header.lower()
		header_value = hdrs[header]
		headers[header_name] = header_value

	return headers

def get_headers_info(headers, header_type='RESPONSE'):
	#the *type* must be passed in.
	_headers_ = []
	headers = format_headers(headers)
	headers_id = generate_id()

	for header in headers:
		h_name = header
		h_value = headers[h_name]
		hv_hash = hashlib.md5(h_value.encode()).hexdigest()
		_headers_.append(
			{'header_id':headers_id, 'header_name':h_name, 'header_value':h_value.upper(), 'header_hash':hv_hash, 'header_type':header_type}
			)

	return _headers_