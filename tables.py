import time

from sqlalchemy import Boolean, Column, Enum, Integer, Interval, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList

Base = declarative_base()

class STable():

	#epoch time
	snapshot_time = Column(Integer, nullable=False)
	#year like 2017, 2018
	snapshot_year = Column(Integer, nullable=False)
	#month value in range 1-12
	snapshot_month = Column(Integer, nullable=False)
	#day value in range 0-31
	snapshot_day = Column(Integer, nullable=False)

	def insert_time(self):
		self.snapshot_time = time.time()
		t = time.gmtime()
		self.snapshot_year = t.tm_year
		self.snapshot_month = t.tm_mon
		self.snapshot_day = t.tm_mday

class Hostname(Base, STable):
	
	__tablename__ = 'hostnames'

	id = Column(Integer, primary_key=True)
	
	#the domain name including its subdomain.
	hostname = Column(String(256), nullable=False)
	#is the subdomain reachable.
	reachability_status = Column(Enum('REACHABLE', 'NOT REACHABLE', 'NOT RESPONDING'), nullable=False)
	#the supported protocols
	supported_protocol = Column(String(8), nullable=False)
	#the ip address.
	ip_address = Column(String(46), nullable=False)
	#the domain name
	domain_name = Column(String(64), nullable=False)
	
	def __repr__(self):
		return "<Hostname(hostname='%s', reachability_status='%s', ip_address='%s')>"%(self.hostname, self.reachability_status, self.ip_address)

class Program(Base, STable):
	
	__tablename__ = 'programs'

	id = Column(Integer, primary_key=True)
	
	program_id = Column(Integer)

	program_name = Column(String(100), nullable=False)
	
	program_url = Column(Text, nullable=False)
	
	program_handle = Column(String(100), nullable=False)
	
	disclosure_url = Column(Text)

	disclosure_email = Column(String(340))

	offers_rewards = Column(Boolean(create_constraint=False))	
	
	offers_thanks = Column(Boolean(create_constraint=False))
	
	internet_bug_bounty = Column(Boolean(create_constraint=False))	
	
	team_type = Column(String(20))


	def __repr__(self):
		return "<Program(handle='%s', name='%s', offers_rewards='%s', team_type='%s', disclosure_email='%s')>"%(self.program_handle, self.program_name, 
			self.offers_rewards, self.team_type, self.disclosure_email
			)

class Asset(Base, STable):
	
	__tablename__ = 'programs'

	id = Column(Integer, primary_key=True)
	
	asset_id = Column(Text, nullable=False)
	
	asset_type = Column(Text, nullable=False)

	#use MutableList here as indicate in 'https://stackoverflow.com/questions/7300230/using-list-as-a-data-type-in-a-column-sqlalchemy'
	asset_identifier = Column(Text, nullable=False)
	
	rendered_instruction = Column(Text)
	
	max_severity = Column(Text, nullable=False)
	
	eligible_for_bounty = Column(Boolean(create_constraint=False))

	in_scope = Column(Boolean(create_constraint=False))

	def __repr__(self):
		return "<Asset(id='%s', asset_identifier='%s', asset_type='%s', max_severity='%s', eligible_for_bounty=%s in_scope=%s)>"%(
			self.asset_id, self.asset_identifier, self.asset_type, 
			self.max_severity, self.eligible_for_bounty, self.in_scope
			)
		
class IPAddress(Base, STable):
	
	__tablename__ = "ipaddress"

	id = Column(Integer, primary_key=True)

	ip_address = Column(String(46), nullable=False)

	address_type = Column(Enum("IPV4","IPV6"), nullable=False)
	
	ports_accessible = Column(Text, nullable=False)

	asn = Column(String(20), nullable=False)

	def __repr__(self):
		return "<IPAddress(ip_address='%s', address_type='%s', asn='%s')>"

class DNSRecord(Base, STable):
	__tablename__ = "dns_records"

	id = Column(Integer, primary_key=True)
	
	name = Column(String(256), nullable=False)

	value = Column(Text, nullable=False)

class WhoisRecord(Base, STable):

	__tablename__ = "whois_records"

	id = Column(Integer, primary_key=True)
	
	name = Column(String(320), nullable=False)
	
	registrar_name = Column(String(256), nullable=False)
	registrant_name = Column(String(256), nullable=False)
	
	registrant_email = Column(String(320), nullable=False)
	registrant_telephone = Column(String(20), nullable=False)
	
	registrant_billing_address = Column(String(100), nullable=False)
	registrant_zipcode = Column(String(10), nullable=False)
	
	#Date in the format: YYYY-MM-DD
	registration_date = Column(String(20), nullable=False)
	
	#Epoch time
	registration_time = Column(Integer, nullable=False)
	
	#Year
	registration_year = Column(Integer, nullable=False)
	
	#Month
	registration_month = Column(Integer, nullable=False)

	#Date in the format: YYYY-MM-DD
	expiration_date = Column(String(20), nullable=False)
	
	#Epoch time
	expiration_time = Column(Integer, nullable=False)
	
	#Year
	expiration_year = Column(Integer, nullable=False)
	
	#Month
	expiration_month = Column(Integer, nullable=False)


class Certificate(Base, STable):

	__tablename__ = "certificates"

	id = Column(Integer, primary_key=True)
	
	issuer_common_name = Column(Text, nullable=False)
	issuer_organization_name = Column(Text, nullable=False)
	issuer_country_name = Column(Text, nullable=False)
	issuer_locality = Column(Text, nullable=True)
	issuer_state = Column(Text, nullable=True)

	subject_common_name = Column(Text, nullable=False)
	subject_organization_name = Column(Text, nullable=False)
	subject_country_name = Column(Text, nullable=False)
	subject_state = Column(Text, nullable=True)
	subject_locality = Column(Text, nullable=True)

	not_before = Column(Integer, nullable=False)
	not_after = Column(Integer, nullable=False)

	#512-long hexadecimal characters representing certificate signature.
	signature = Column(Text, nullable=False)
	
	#serial number of the certificate.
	serial_number = Column(Text, nullable=False)

	#md5 hash of the certificate fingerprint.
	fingerprint_md5 = Column(Text, nullable=False)
	
	#sha256 hash of the certificate fingerprint.
	fingerprint_sha256 = Column(Text, nullable=False)

	#',' joined subject_alternative_name.
	subject_alternative_name = Column(Text, nullable=False)

	#the key-generation algorithm.
	public_key_type = Column(String(10), nullable=False)
	
	#the number of bits of the public key.
	public_key_size = Column(Integer, nullable=False)

	#the exponent used in deriving the RSA public key.
	public_key_exponent = Column(Integer, nullable=False)
	
	public_key_x_comp = Column(Integer, nullable=True)
	public_key_y_comp = Column(Integer, nullable=False)
	
	#sha256 hash of the public key itself.
	public_key_hash = Column(Text, nullable=False)

	version_name = Column(String(10), nullable=False)
	version_value = Column(String(10), nullable=False)

class Connection(Base, STable):

	__tablename__ = "connections"

	id = Column(Integer, primary_key=True)
	
	#hostname
	hostname = Column(String(256), nullable=False)

	#port number
	port = Column(Integer, nullable=False)

	#type: http, https, smtp, ftp, ftps
	connection_type = Column(String(15), nullable=False)

	#cipher used during the connection.
	connection_cipher = Column(String(30), nullable=True)
	
	#tls version used during the connection.
	connection_tls_version = Column(String(30), nullable=True)
	
	connection_tls_bits = Column(Integer, nullable=True)
	
	# '|' concatenated list of ciphersuites supported.
	ciphersuites = Column(Text, nullable=True)

	#an hash of ciphersuites
	ciphersuites_hash = Column(Text, nullable=True)

	#ja3 signature.
	ja3_signature = Column(Text, nullable=True)

	connection_tls_cert_hash = Column(Text, nullable=True)

class HTMLFilter(Base, STable):

	__tablename__ = "html_filters"
	
	id = Column(Integer, primary_key=True)

	page_id = Column(String(40), nullable=False)

	page_domain = Column(Text, nullable=False)
	
	page_path = Column(Text, nullable=False)

	filter_name = Column(Text, nullable=False)

	filter_value = Column(Text, nullable=True)

class HTTPHeader(Base, STable):

	__tablename__ = "http_headers"

	id = Column(Integer, primary_key=True)
	
	hostname = Column(Text, nullable=False)
	
	path = Column(Text, nullable=False)

	url = Column(Text, nullable=False)

	header_name = Column(Text, nullable=False)
	
	header_value = Column(Text, nullable=False)

	header_name_hash = Column(Text, nullable=False)

	header_value_hash = Column(Text, nullable=False)


class HTMLPage(Base, STable):

	__tablename__ = "html_pages"

	id = Column(Integer, primary_key=True)

	page_domain = Column(Text, nullable=False)
	
	page_tags = Column(Text, nullable=False)

	page_path = Column(Text, nullable=False)

	page_title = Column(Text, nullable=False)

	page_title_hash = Column(Text, nullable=False)
	
	page_size = Column(Integer, nullable=False)

	page_hash = Column(Text, nullable=False)

	#head or header tag
	# page_header = Column(Text, nullable=False)
	
	#footer tag 
	# page_footer = Column(Text, nullable=False)

class HTMLLink(Base, STable):

	__tablename__ = "html_links"

	id = Column(Integer, primary_key=True)

	#script, link, anchor, image
	link_type = Column(Text, nullable=False)
	
	#href, src, action
	link_attribute = Column(Text, nullable=False)

	#http://example.com/hello/word/
	link_source_url = Column(Text, nullable=False)

	#/js/login.js
	link_url = Column(Text, nullable=False)
	


class Website(Base, STable):

	__tablename__ = "websites"

	id = Column(Integer, primary_key=True)

	website_name = Column(Text, nullable=False)

	website_protocol = Column(Text, nullable=False)
	
	website_port = Column(Integer, nullable=False)


class Port(Base, STable):

	__tablename__ = "ports"

	id = Column(Integer, primary_key=True)

	ip = Column(Text, nullable=False)

	hostname = Column(Text, nullable=True)
	
	status = Column(Text, nullable=False)

	port = Column(Integer, nullable=False)
	
	connect_latency = Column(Integer, nullable=False)

	recieve_latency = Column(Integer, nullable=False)

	port_name = Column(Text, nullable=True)

	#first 1024 recieved bytes.
	recieved_bytes = Column(Text, nullable=True)
	
	recieved_bytes_hash = Column(Text, nullable=True)

class DNSFilter(Base, STable):

	__tablename__ = "dns_filters"
	
	id = Column(Integer, primary_key=True)

	domain_id = Column(String(40), nullable=False)

	domain = Column(Text, nullable=False)
	
	filter_name = Column(Text, nullable=False)

	filter_value = Column(Text, nullable=True)


class CertificateFilter(Base, STable):

	__tablename__ = "certificate_filters"

	id = Column(Integer, primary_key=True)
	
	#id used to identify the certificate the filter belongs to.
	transaction_id = Column(String(40), nullable=False)
	
	domain = Column(Text, nullable=False)
	
	filter_name = Column(Text, nullable=False)

	filter_value = Column(Text, nullable=True)

class WHOIS_Filter(Base, STable):

	__tablename__ = "whois_filters"
	
	id = Column(Integer, primary_key=True)

	#id used to identify the record the filter belongs to.
	transaction_id = Column(String(40), nullable=False)

	domain = Column(Text, nullable=False)
	
	filter_name = Column(Text, nullable=False)

	filter_value = Column(Text, nullable=True)

class Header(Base, STable):

	__tablename__ = "headers"
	
	id = Column(Integer, primary_key=True)

	#id to identify the response the header belongs to.
	transaction_id = Column(String(40), nullable=False)
	
	header_type = Column(Enum('REQUEST', 'RESPONSE'), nullable=False)

	header_name = Column(Text, nullable=False)

	header_value = Column(Text, nullable=False)
	
	#md5 hash of the header value.
	header_hash = Column(String(32), nullable=False)

