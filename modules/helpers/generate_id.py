import secrets


def generate_id(size=40):
	return secrets.token_hex(size)
