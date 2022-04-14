
from drift.tables import Hostname as HostnameTable


class Hostname:

	def __init__(self, hostname, reachability_status, supported_protocol, ip_address, domain_name):
		#the domain name including its subdomain.
		self.hostname = hostname

		#is the subdomain reachable.
		self.reachability_status = reachability_status

		#the supported protocols
		self.supported_protocol = supported_protocol

		#the ip address.
		self.ip_address = ip_address

		#the domain name
		self.domain_name = domain_name

	def get_hostname(self):
		return self.hostname.lower()

	def set_hostname(self, hostname):
		self.hostname = hostname.lower()
		return self

	def get_reachability_status(self):
		return self.reachability_status.upper()

	def set_reachability_status(self, reachability_status):
		self.reachability_status = reachability_status.upper()
		return self

	def get_supported_protocol(self):
		return self.supported_protocol.upper()

	def set_supported_protocol(self, supported_protocol):
		self.supported_protocol = hostname.upper()
		return self

	def get_ip_address(self):
		return self.ip_address.upper()

	def set_ip_address(self, ip_address):
		self.ip_address = ip_address.upper()
		return self

	def get_domain_name(self):
		return self.domain_name.lower()

	def set_domain_name(self, domain_name):
		self.domain_name = domain_name.lower()
		return self
	
	def create_record(self):
		return HostnameTable(
			hostname=self.get_hostname(), reachability_status = self.get_reachability_status(),
			supported_protocol=self.get_supported_protocol(), ip_address=self.get_ip_address(),
			domain_name=self.get_domain_name()
			)
