from urllib.request import urlparse


class CredentialStorage(object):

	def __init__(self):
		self.credential_storage = {}
	
	def add_credentials(self,domain,data=None,json=None,headers={},paths=['*'],protocols=['*'],**kwargs):
		
		credentials = {}
		
		credentials[domain] = {'data':data,'json':json,'headers':headers,'paths':paths,'protocols':protocols,**kwargs}
		
		self.credential_storage.update(credentials)
		
		return True
	
	def get_credentials(self,domain):
		return self.credential_storage.get(domain,None)
	
	def credentials_exist(self,domain):
		
		if self.credential_storage.get(domain,None):
			return True
		else:
			return False
	
	def resolve_credentials(self,url):
		
		parsed_url = urlparse(url)
		domain = parsed_url.netloc
		
		protocol = parsed_url.scheme
		path = parsed_url.path
		domain = domain.strip('.')
		
		if self.credentials_exist(domain):
			
			credentials = self.get_credentials(domain)
			
			paths = credentials['paths']
			protocols = credentials['protocols']
			
			condition_1 = path and paths.count('*') > 0 or paths.count(path) > 0
			condition_2 = protocol and protocols.count('*') > 0 or protocols.count(protocol) > 0
			
			if condition_1 and condition_2:
				return credentials
		else:
			return None

cs = CredentialStorage()

cs.add_credentials('google.com',data={'username':'username','password':'password'})

