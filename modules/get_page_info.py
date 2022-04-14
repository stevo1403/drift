
from .helpers.pages import (Anchors, Areas, Audios, Embeds, Forms, IFrames,
                            Images, Links, Metas, Objects, Scripts, Styles,
                            SVGs, Videos, convert_page, get_base, get_icons,
                            get_title, parse_data)


class PageHandler:

	def __init__(self, html):
		self.html = html
		self.page = None
		self.elements = [
		Forms, Links, Anchors, Areas, Metas, Scripts, 
		Images, Videos, Audios, IFrames, Objects, Embeds,
		SVGs, Styles
		]

		self.special_elements = [
		get_title, get_base, get_icons
		]
		
		self.init()

	def init(self):
		self.page = convert_page(self.html)

	def get_filters(self):
		filters = []

		for element in self.elements:

			e = element(self.page)
			tag_name = e.tag_name
			element_filters = e.extract()
			data = parse_data(element_filters, tag_name)

			if data:
				filters.append(data)
		
		for element in self.special_elements:
			tag_name, element_filters = element(self.page)
			data = parse_data(element_filters, tag_name)
			
			if data:
				filters.append(data)

		return filters