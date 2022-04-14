from urllib.parse import urlparse

from drift.functions.generate_id import generate_id
from drift.modules.get_page_info import PageHandler
from drift.tables import HTMLFilter as PageTable


class Filter:
	def __init__(self, name, value, page_id, page_url):
		self.name = name
		self.value = value
		self.page_id = page_id
		self.page_url = page_url

	def get_name(self):
		return self.name.lower()

	def set_name(self, name):
		self.name = name.lower()
		return self

	def get_value(self):
		return self.value

	def set_value(self, value):
		self.value = value
		return self

	def get_page_id(self):
		return self.page_id.lower()

	def set_page_id(self, page_id):
		self.page_id = page_id.lower()

	def get_page_url(self):
		return self.page_url.lower()

	def set_page_url(self, page_url):
		self.page_url = page_url.lower()
	
	def get_page_domain(self):
		return urlparse(self.page_url).netloc

	def get_page_path(self):
		return urlparse(self.page_url).path or '/'

	def create_record(self):
		return PageTable(
			filter_name=self.get_name(), filter_value=self.get_value(), 
			page_id=self.get_page_id(), page_domain=self.get_page_domain(),
			page_path=self.get_page_path(),
			)

class Page:
	def __init__(self, html, url):
		self.html = html
		self.url = url

	def get_records(self):

		records = []

		ph = PageHandler(self.html)

		filters = ph.get_filters()

		page_id = generate_id(40)

		for element in filters:

			for _filter in element:

				filter_name = _filter[0]
				filter_value = _filter[1]

				_filter = Filter(name=filter_name, value=filter_value, page_id=page_id, page_url=self.url)
				record = _filter.create_record()
				record.insert_time()

				records.append(record)

		return records