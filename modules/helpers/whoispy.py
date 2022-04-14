import json
import os
import re
import socket
import sys

import sqlalchemy
from sqlalchemy import Boolean, Column, Enum, Integer, Interval, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .whois_config import config

Base = declarative_base()


MAIN_DIR = os.path.dirname(__file__)

whois_server_db = os.path.join(MAIN_DIR, 'whois-servers.db')

engine = sqlalchemy.create_engine('sqlite:///%s'%(whois_server_db))
Session = sessionmaker(bind=engine)

class Whois(Base):
	
	__tablename__ = 'whois'

	id = Column(Integer, primary_key=True)
	tld = Column(String(20), nullable=False, unique=True)
	whois_server = Column(String(250), nullable=False)

def delete_tables(checkfirst=True):

	session = Session()
	Base.metadata.drop_all(engine, Base.metadata.tables.values(), checkfirst=checkfirst)
	session.flush()
	session.commit()
	session.close()

def create_tables(checkfirst=True):
	session = Session()
	Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=checkfirst)
	session.flush()
	session.commit()
	session.close()
	
def insert_records():
	session = Session()
	whois_file = os.path.join(MAIN_DIR, 'whois-servers.txt')
	
	with open(whois_file, 'rt') as f:
		for line in f:
			line = line.strip()
			if line and not line.startswith(';'):
				tld, addr = line.split(' ', 1)
				w = Whois(tld=tld, whois_server=addr)
				session.add(w)

	session.flush()
	session.commit()

def insert_record(tld, server_addr):
	session = Session()
	session.add(Whois(tld=tld, whois_server=server_addr))
	session.flush()
	session.commit()

def get_record(tld):
	session = Session()
	result = session.query(Whois).filter(Whois.tld == tld)
	for row in result:
		return row.whois_server

result = """
	Domain Name: creditsync.com.ng
	Registry Domain ID: 1668901-NIRA
	Registry WHOIS Server:: whois.nic.net.ng
	Registrar URL: http://www.domainking.ng
	Updated Date: 2020-12-08T09:24:28.961Z
	Creation Date: 2020-11-06T19:51:48.404Z
	Registry Expiry Date: 2021-11-06T19:51:48.640Z
	Registrar Registration Expiration Date: 2021-11-06T19:51:48.640Z
	Registrar: DomainKing
	Registrar IANA ID: 28112014
	Registrar Abuse Contact Email: support@domainking.ng
	Registrar Abuse Contact Phone: +91.9646369965
	Registrar Country: IN
	Registrar Phone: +91.9646369965
	Registrar Customer Service Contact: DomainKing.NG Support
	Registrar Customer Service Email: support@domainking.ng
	Registrar Admin Contact: DomainKing.NG
	Registrar Admin Email: dk@hannu.co
	Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited
	Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
	Registry Registrant ID: dBVHk-qSeIp
	Registrant Name: Creditsync
	Registrant Organization: Creditsync
	Registrant Street: Ekiti
	Registrant City: Ado
	Registrant State/Province: Ekiti
	Registrant Postal Code: 5088
	Registrant Country: NG
	Registrant Phone: +234.8057897678
	Registrant Email: support@creditsync.com.ng
	Registry Admin ID: 3E7TB-CUDLB
	Admin Name: Creditsync
	Admin Organization: Creditsync
	Admin Street: Ekiti
	Admin City: Ado
	Admin State/Province: Ekiti
	Admin Postal Code: 5088
	Admin Country: NG
	Admin Phone: +234.8057897678
	Admin Email: support@creditsync.com.ng
	Registry Tech ID: Ib3Ax-czI0f
	Tech Name: Creditsync
	Tech Organization: Creditsync
	Tech Street: Ekiti
	Tech Street: Ekiti
	Tech City: Ado
	Tech State/Province: Ekiti
	Tech Postal Code: 5088
	Tech Country: NG
	Tech Phone: +234.8057897678
	Tech Email: support@creditsync.com.ng
	Registry Billing ID: A2be0-TXDOi
	Billing Name: Creditsync
	Billing Organization: Creditsync
	Billing Street: Ekiti
	Billing Street: Ekiti
	Billing City: Ado
	Billing State/Province: Ekiti
	Billing Postal Code: 5088
	Billing Country: NG
	Billing Phone: +234.8057897678
	Billing Email: support@creditsync.com.ng
	Name Server: ns1.digitalocean.com
	Name Server: ns2.digitalocean.com
	Name Server: ns3.digitalocean.com
	DNSSEC: unsigned
"""

def create_structure(config):

	data = {}
	for rule in config:
		
		key = rule.get('key')
		action = rule.get('action')
		sections = key.split('.')
		
		d = data
		
		for index, section in enumerate(sections):
			if not d.get(section):
				
				if index == len(sections)-1:
					d[section] = []

				else:
					d[section] = {}

			d = d[section]

	return data

def insert_data(structure, key, value, action):
	sections = key.split('.')
	d = structure
	for index, section in enumerate(sections):
		d = d[section]
		if index == len(sections) -1:
			if action == 'replace':
				d.clear()

			if not value in d:
				d.append(value)
	
	return structure

def split_words(text):
	words = text.split(' ')
	
	while '' in words:
		words.remove('')

	return words

def match(field, rule):
	
	patterns = rule.get('patterns')
	words = rule.get('words')
	texts = rule.get('texts')
	strict = rule.get('strict')

	if strict == None:
		strict = False

	if not strict:
		flags = re.IGNORECASE
	else:
		flags = 0

	result = {
		'patterns':None,
		'words':None,
		'texts':None
	}

	if not field:
		return result

	if patterns:
		result['patterns'] = False
		for pattern in patterns:
			if re.match(pattern, field, flags):
				result['patterns'] = True

	if words:
		field_words = split_words(field)
		
		if not strict:
			field_words = [word.lower() for word in field_words]

		if field_words:
			result['words'] = False

		for word_group in words:
			
			passed = False

			for word in word_group:

				if not strict:
					word = word.lower()

				if not word in field_words:
					passed = False
					#stop the search and go to the next group.
					break
				else:
					passed = True

			if passed:
				result['words'] = True
				break
			else:
				result['words'] = False


	if texts:
		if not strict:
			field = field.lower()
		
		result['texts'] = False

		for text in texts:
			if not strict:
				text = text.lower()
			
			if field == text:
				result['texts'] = True

	return result

def make_connection(whois_server, command):
	with socket.create_connection((whois_server, 43), timeout=5) as s:
		s.send(command.encode())
		s.settimeout(5)
		message = b""

		while True:
			m = s.recv(2048)
			if not m:
				break
			else:
				message += m

		return message

def parse_record_for_server(record):
	lines = record.split('\n')
	for line in lines:
		line = line.strip()
		if line and not line.startswith('%') and not line.startswith(';'):
			if line.startswith('whois:'):
				fields = line.split(':', 1)
				if len(fields) == 2:
					return fields[-1].strip()

def get_tld(hostname):
	hostname = hostname.encode('idna').decode('utf-8')
	tld = hostname.split('.')[-1]
	return tld

def get_whois_server(hostname):
	tld = get_tld(hostname)
	if tld:
		server = get_record(tld)
		if not server:
			record = make_connection('whois.iana.org', hostname+'\r\n')
			server = parse_record_for_server(record)
			insert_record(tld, server)
			return server
		else:
			return server

def clean_hostname(string):
	allowed_chars = ['.', '-']
	chars = ""
	for char in string:
		if char.isalnum() or char in allowed_chars:
			chars += char
	
	return chars

def get_whois_server_from_record(record):
	words = ['whois', 'server']
	lines = record.split('\n')
	for line in lines:
		line = line.strip()
		fields = line.split(':', 1)
		if len(fields) == 2:
			field_name = fields[0]
			field_value = fields[1]
			passed = True
			for word in words:
				if not word.lower() in field_name.lower():
					passed = False
			if passed:
				return field_value.strip()

def get_whois_record(hostname, with_data=True):

	server = get_whois_server(hostname)
	if server:
		record = make_connection(server, hostname+'\r\n')
		record = record.decode('utf-8')
		
		if with_data:
			server = get_whois_server_from_record(record)
			server = clean_hostname(server)
			try:
				record = make_connection(server, hostname+'\r\n')
			except Exception:
				pass
			return record.decode('utf-8')
		else:
			return record.decode('utf-8')
	else:
		return None

def format_record(record):
	
	record = record.split('\n\n')[0]
	fields = []

	for line in record.split('\n'):
		fields.append(line.strip())

	data = create_structure(config)
	for field in fields:
		f = field.split(': ', 1)
		
		if len(f) == 2:
			#there is a field name and field value
			field_name = f[0].strip()
			field_value = f[1]

			#clean up field names that has two colon(::) appended to it.
			field_name = field_name.rstrip(':').strip()

			for char in field_name:
				#char is not alphanumeric and char is not space.
				if not char.isalnum() and not char.isspace():
					field_name = None
					field_value = None
					break
		else:
			#well there are no fields, just free text.
			field_name = None
			field_value = None

		for rule in config:
			target = rule.get('target')
			action = rule.get('action')

			if target:
				field_name_rule = target.get('FIELD_NAME')
				field_value_rule = target.get('FIELD_VALUE')
				field_rule = target.get('ALL')
				
				matched = None

				if field_name_rule:
					m = match(field_name, field_name_rule)
					if True in m.values():
						key = rule.get('key')
						matched = True
						insert_data(data, key, field_value, action)

				if field_value_rule and not matched:
					m = match(field_value, field_value_rule)
					if True in m.values():
						key = rule.get('key')
						matched = True
						insert_data(data, key, field_value, action)

				if field_rule and not matched:
					m = match(field, field_rule)
					if True in m.values():
						key = rule.get('key')
						insert_data(data, key, field_value, action)

	return data

"""
TODO:
1) Convert the date format.
"""

def parse_data(data, name=""):
	
	values = []

	if type(data) == dict:
		for k in data:
			
			v = data[k]
			n = name + '.' + str(k)
			n = n.lower()
			r = parse_data(v, n)

			if type(r) == list and len(r):
				values.extend(r)
			else:
				vv = (n, r)
				values.append(vv)

		return values

	elif type(data) == list:
		n = name
		
		n = n.lower()

		for item in data:
			r = parse_data(item, n)

			if type(r) == list and len(r):
				values.extend(r)
			else:
				vv = (n, r)
				values.append(vv)

		return values
	
	elif data == None:
		return None

	else:
		return str(data)

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print('Usage: %s <hostname>,[<hostname>,<hostname>]'%sys.argv[0])
	else:
		hostnames = sys.argv[1:]
		for hostname in hostnames:
			hostname = hostname.strip()
			try:
				record = get_whois_record(hostname)
				if not record:
					tld = get_tld(hostname)
					print("Error: Cannot find the whois server responsible for hostname '%s' whose tld is '%s'."%(hostname, tld))
					continue
				
				data = format_record(record)
				data = parse_data(data, 'dns')
				
				for l in data:
					l0 = l[0]
					l1 = l[1]
					print("%s: %s"%(l0, l1))
					print()


			except Exception as e:
				print("Error: Failed to retrieve whois record for host %s due to '%s'."%(hostname, e))
