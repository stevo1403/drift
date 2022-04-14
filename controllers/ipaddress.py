from drift.tables import IPAddress as IPAddressTable


class IPAddress:
	def __init__(self, ip_address, address_type, ports_accessible, asn):

		self.ip_address = ip_address 

		self.address_type = address_type 

		self.ports_accessible = ports_accessible 

		self.asn = asn 

	def get_ip_address(self):
		return self.ip_address.upper()

	def set_ip_address(self, ip_address):
		self.ip_address = ip_address.upper()
		return self

	def get_address_type(self):
		return self.address_type.upper()

	def set_address_type(self, address_type):
		self.address_type = address_type or -1
		return self

	def get_ports_accessible(self):
		return self.ports_accessible

	def set_ports_accessible(self, ports_accessible):
		self.ports_accessible = ports_accessible
		return self

	def get_asn(self):
		return self.asn.upper()

	def set_asn(self, asn):
		self.asn = asn.upper()
		return self

	def create_record(self):
		return IPAddressTable(
			ip_address=self.get_ip_address(), address_type=self.get_address_type(), ports_accessible=self.get_ports_accessible(),
			asn=self.get_asn()
			)
