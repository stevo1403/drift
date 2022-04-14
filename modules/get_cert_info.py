import hashlib
import json
import socket
import ssl

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import (dh, dsa, ec, ed448,
                                                       ed25519, rsa, x448,
                                                       x25519)
from cryptography.x509 import extensions
from cryptography.x509.oid import (AuthorityInformationAccessOID, ExtensionOID,
                                   NameOID)

__all__ = ['get_cert_info', 'get_cert_info_by_addr']

def get_attributes(s):
	subject_attr = {}
	for attribute in list(s):
		subject_attr[attribute.oid._name] = attribute.value

	return subject_attr

def extract_san(cert):
	domain_names = set()
	for extension in cert.extensions:
		if extension.oid == ExtensionOID.SUBJECT_ALTERNATIVE_NAME:
			dns_names = list(extension.value)
			for dns_name in dns_names:
				domain_names.add(dns_name.value)

	return list(domain_names)

def extract_crl(cert):
	crls = []
	for extension in cert.extensions:
		if extension.oid == ExtensionOID.CRL_DISTRIBUTION_POINTS:
			distribution_points = list(extension.value)
			for distribution_point in distribution_points:
				crl = {
					'crl_issuer':distribution_point.crl_issuer, 'relative_name':distribution_point.relative_name,
					'full_name':[name.value for name in distribution_point.full_name], 'reasons':distribution_point.reasons
					}
				crls.append(crl)

	return crls

def extract_authority_info(cert):
	authority_info = {}
	for extension in cert.extensions:
		if extension.oid == ExtensionOID.AUTHORITY_INFORMATION_ACCESS:
			authority_info_asset_list = list(extension.value)
			for auth_info in authority_info_asset_list:
				if hasattr(auth_info, 'access_method') and hasattr(auth_info, 'access_location'):
					authority_info[auth_info.access_method._name] = [auth_info.access_location.value]

	
	return authority_info

def get_cert_info(raw_cert, cert_type='pem'):

	if cert_type == 'pem':
		c = x509.load_pem_x509_certificate(raw_cert)
	else:
		c = x509.load_der_x509_certificate(raw_cert)

	subject = c.subject
	issuer = c.issuer

	sans = extract_san(c)

	crls = extract_crl(c)

	auth_info = extract_authority_info(c)

	not_valid_before = c.not_valid_before
	not_valid_after = c.not_valid_after

	fingerprint = c.fingerprint
	serial_number = c.serial_number
	version = c.version
	fingerprint = c.fingerprint
	signature = c.signature.hex()

	public_bytes = c.public_bytes(serialization.Encoding.PEM)


	"Server Certificate contains the public key."

	public_key_size = c.public_key().key_size

	if isinstance(c.public_key(), rsa.RSAPublicKey):
		public_key_type = 'RSA'
	elif isinstance(c.public_key(), dsa.DSAPublicKey):
		public_key_type = 'DSA'
	elif isinstance(c.public_key(), dh.DHPublicKey):
		public_key_type = 'DH'
	elif isinstance(c.public_key(), ec.EllipticCurvePublicKey):
		public_key_type = 'EC'
	elif isinstance(c.public_key(), x448.X448PublicKey):
		public_key_type = 'X448'
	elif isinstance(c.public_key(), x25519.X25519PublicKey):
		public_key_type = 'X25519'
	elif isinstance(c.public_key(), ed25519.ED25519PublicKey):
		public_key_type = 'ED25519'
	elif isinstance(c.public_key(), ed448.ED448PublicKey):
		public_key_type = 'ED448'
	else:
		public_key_type = 'UNKNOWN'

	if public_key_type == 'RSA':
		public_key = c.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.PKCS1)
		public_key_exponent = c.public_key().public_numbers().e
	else:
		public_key = c.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
		public_key_exponent = 0

	public_key_x_comp = 0
	public_key_x_comp = 0

	if public_key_type == 'EC':
		public_key_x_comp = c.public_key().public_numbers().x
		public_key_y_comp = c.public_key().public_numbers().y


	subject_attr = get_attributes(subject)
	issuer_attr = get_attributes(issuer)

	public_key_hash = hashlib.sha256(public_key).hexdigest()

	fingerprint_md5 = fingerprint(hashes.MD5()).hex()
	fingerprint_sha256 = fingerprint(hashes.SHA256()).hex()

	cert_attr = {
		'key_type':public_key_type,
		'key_size':public_key_size,
		'key_exponent':public_key_exponent,
		'key_hash':public_key_hash,
		'subject':subject_attr,
		'issuer':issuer_attr,
		'not_before':not_valid_before.timestamp(),
		'not_after':not_valid_after.timestamp(),
		'signature':signature,
		'fingerprint_md5':fingerprint_md5,
		'fingerprint_sha256':fingerprint_sha256,
		'serial_number':str(serial_number),
		'version_name':version.name,
		'version_value':version.value,
		'crl':crls,
		'auth_info':auth_info,
		'subject_alternative_name':sans
	}

	return cert_attr


def get_cert_info_by_addr(hostname, port, timeout=10, strict=False):
	context = ssl.create_default_context()
	s = socket.create_connection((hostname, port), timeout=timeout)
	if not strict:
		context.check_hostname = False
		context.verify_mode = ssl.VerifyMode.CERT_NONE

	sock = context.wrap_socket(s, server_hostname=hostname)
	return dict(get_cert_info(sock.getpeercert(binary_form=True), 'der'))

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
