import dns.resolver

__ALL__ = ['get_dns_info']

def create_dns_resolver(timeout):
	
	"""
	Returns a resolver of type dns.resolver.Resolver.
	@param timeout: the amount of time(in seconds.) to wait for dns response before timing out.
	@type timeout: int  
	@rtype resolver: dns.resolver.Resolver | None
	"""

	resolver = dns.resolver.Resolver()
	resolver.timeout = timeout
	return resolver

def make_dns_query(hostname, record_type, resolver=None, timeout=5):
	"""
	Returns dns.resolver.Answer object as response or an exception if an unhandled exception occurs. 
	Otherwise it returns a string which indicates the error type.
	
	@param hostname: the hostname whose dns record is to be retrieved.
	@type hostname: str
	@param record_type: the type of dns record to query. Accepted values are: 
		A, AAAA, CNAME, NS, TXT, MX, SOA, PTR, CERT, DNSKEY, DS, SRV
	@type record_type: str
	@param resolver: the resolver object to use for querying dns records.
	@type resolver: dns.resolver.Resolver | None
	@param timeout: the amount of time(in seconds.) to wait for dns response before timing out.
	@type timeout: int  
	@rtype: dns.resolver.Answer | str | None
	"""

	if not resolver:
		resolver = create_dns_resolver(timeout)
	try:
		response = resolver.query(hostname, record_type, raise_on_no_answer=True)
		return response
	except dns.resolver.Timeout:
		return "Error::TIMEOUT"
	except dns.resolver.NXDOMAIN:
		return "Error::DOMAIN_DOES_NOT_EXIT"
	except dns.resolver.YXDOMAIN:
		return "Error::DOMAIN_NAME_TOO_LONG"
	except dns.resolver.NoAnswer:
		return "Error::NO_ANSWER"
	except dns.resolver.NoNameservers:
		return "Error::NO_NAMESERVERS"
	except Exception as e:
		print("[-] DNS Exception: %s"%(e))
		return e

def get_dns_info(hostname, timeout=5):
	
	"""
	@param hostname: the hostname whose dns record is to be retrieved.
	@type hostname: str
	@param timeout: the amount of time(in seconds.) to wait for dns response before timing out.
	@type timeout: int 
	"""
	
	resolver = create_dns_resolver(timeout)
	result = {}
	record_types = ['A','AAAA','CNAME','SOA','MX','TXT', 'NS', 'CERT', 'DNSKEY', 'DS', 'SRV']

	for record_type in record_types:
		dns_response = make_dns_query(hostname, record_type, resolver, timeout)

		if type(dns_response) == dns.resolver.Answer:
			result[record_type] = [str(resp) for resp in dns_response]
		else:
			result[record_type] = []


	return result
