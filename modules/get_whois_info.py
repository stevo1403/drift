from .helpers.whoispy import format_record as format_whois_record
from .helpers.whoispy import get_whois_record as _get_whois_record
from .helpers.whoispy import parse_data as parse_whois_data


def get_whois_record(hostname):
	
	"""
	Returns a list which which contains named tuple(s).
	@param hostname: the hostname whose whois record is to be retrieved.
	@type hostname: str
	@rtype list
	"""

	data = {}
	try:
		record = _get_whois_record(hostname)
		if record:
			data = format_whois_record(record)
			data = parse_whois_data(data)
			data = [tuple(r) for r in data]
	except Exception as e:
		print('Exception: ', e)
	
	return data

