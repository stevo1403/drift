import json
import pprint
import ssl

host = 'google.com'
port = 443

# conn = ssl.create_connection((host, port))
# context = ssl.create_default_context()
# sock = context.wrap_socket(conn, server_hostname=host)

def save_file(content, filename='test.json'):
	with open(filename, 'wt', encoding='utf-8') as f:
		json.dump(content, f)
		return filename

def load_file(filename='test.json'):
	with open(filename, 'rt', encoding='utf-8') as f:
		return json.load(f)

# cert = sock.getpeercert()
# save_file(cert)

cert = load_file()

subject = cert['subject']
version = cert['version']
ocsp = cert['OCSP']
ca_issuers = cert['caIssuers']
crl_distribution_points = cert['crlDistributionPoints']
not_after = cert['notAfter']
not_before = cert['notBefore']
serial_number = cert['serialNumber']
subject_alternative_name = cert['subjectAltName']
issuer = cert['issuer']


def get_mapping(fields):
	mapping = {}
	for section in fields:
		for field in section:
			field_name, field_value = field
			if field_name in mapping:
				mapping[field_name].append(field_value)
			else:
				mapping[field_name] = [field_value]

	return mapping

print('Subject: ', get_mapping(subject) )
print()
print('Issuer: ', get_mapping(issuer) )
print()
print('SAN: ' , get_mapping([subject_alternative_name]) )