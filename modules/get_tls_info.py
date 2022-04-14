import hashlib
import socket
import ssl

from . import hash_cert


def get_tls_info_by_addr(hostname, port, timeout=10):
	context = ssl.create_default_context()
	s = socket.create_connection((hostname, port), timeout=timeout)
	sock = context.wrap_socket(s, server_hostname=hostname)
	return get_tls_info(sock)

def get_tls_info(socket):
	info = {}

	tls_cipher = socket.cipher()[0] or ''
	tls_version = socket.cipher()[1] or ''
	tls_bits = socket.cipher()[2]
	
	tls_cert_hash = hash_cert.get_cert_hash(socket.getpeercert(1))

	cipher_suite = tls_cipher.upper() + tls_version + str(tls_bits)
	tls_ciphersuite_hash = hashlib.md5(cipher_suite.encode('utf-8')).hexdigest()
	
	info['tls_cipher'] = tls_cipher.upper()
	info['tls_version'] = tls_version.upper()
	info['tls_bits'] = tls_bits
	info['tls_cert_hash_md5'] = tls_cert_hash['md5'].lower()
	info['tls_cert_hash_sha1'] = tls_cert_hash['sha1'].lower()

	info['tls_ciphersuite_hash'] = tls_ciphersuite_hash.lower()

	return info
