import hashlib


def get_cert_hash(encoddd_cert):

	return {
	'md5':hashlib.md5(encoddd_cert).hexdigest(), 
	'sha1':hashlib.sha1(encoddd_cert).hexdigest()
	}
