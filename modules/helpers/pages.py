import hashlib

from bs4 import BeautifulSoup, Comment


class Forms:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""

		self.page = page
		self.forms = []
		
		self.tag_name = 'form'

	def get_text_areas(self, form):

		text_areas = form.findAll('textarea')
		txt_areas = []

		for text_area in text_areas:
			_txt_ = {}

			_txt_['name'] = text_area.get('name')
			_txt_['type'] = text_area.get('type')
			_txt_['placeholder'] = text_area.get('placeholder')

			txt_areas.append(_txt_)

		return txt_areas

	def get_selects(self, form):

		selects = form.findAll('select')
		slcts = []

		for select in selects:
			
			slt = {}
			
			slt['name'] = select.get('name')
			slt['multiple'] = True if select.get('multiple') != None else False
			slt['size'] = select.get('size')
			slt['value'] = ''

			options = []

			for option in select.findAll('option'):
				options.append(option.get('value'))
				if option.get('selected') is not None:
					slt['value'] = option.get('value')

			slt['options'] = options
			slcts.append(slt)

		return slcts

	def get_inputs(self, form):

		inputs = form.findAll('input')
		inpts = []

		for input_ in inputs:
			inpt = {}
			#specify the name of the input field.
			inpt['name'] = input_.get('name')
			#specify the type of the input field.
			inpt['type'] = input_.get('type')
			#specify the value of the input field.
			inpt['value'] = input_.get('value')
			#comma separated list of accepted extensions and mime types when type=file.
			inpt['accept'] = input_.get('accept')
			#specify the media capture input method when type=file. Can be either user or environment.
			inpt['capture'] = input_.get('capture')
			#specify the name of the form field to be used while sending the input elements directionality to the server.
			inpt['dirname'] = input_.get('dirname')
			#specify the maximum length of the text allowed in the field.
			inpt['maxlength'] = input_.get('maxlength')
			#specify the minimum length of the text allowed in the field.
			inpt['minlength'] = input_.get('minlength')
			#specify that multiple values are allowed.
			inpt['multiple'] = True if input_.get('multiple') != None else False
			#specify that pattern to match the input's value against.
			inpt['pattern'] = input_.get('pattern')
			#specify the placeholder of the input field.
			inpt['placeholder'] = input_.get('placeholder')
			#specify the src of the image when type=image.
			inpt['src'] = input_.get('src')
			#gives advisory information.
			inpt['title'] = input_.get('title')

			inpts.append(inpt)

		return inpts

	def get_buttons(self, form):

		buttons = form.findAll('button')
		btns = []

		for button in buttons:
			_btn_ = {}

			_btn_['name'] = button.get('name')
			_btn_['type'] = button.get('type')
			_btn_['value'] = button.get('value')
			
			btns.append(_btn_)
		
		return btns

	def extract(self):

		page_forms = self.page.findAll(name='form')
		forms = []

		for form in page_forms:

			frm = {}
			
			_text = form.text.strip()

			while '\n\n' in _text:
				_text = _text.replace('\n\n', '\n')

			_hash = hashlib.md5(_text.encode()).hexdigest()

			frm['method'] = form.get('method')
			
			frm['text'] = _text
			frm['hash'] = _hash

			frm['action'] = form.get('action')
			frm['enctype'] = form.get('enctype')
			frm['hidden'] = form.get('hidden')

			frm['buttons'] = self.get_buttons(form)
			frm['inputs'] = self.get_inputs(form)
			frm['selects'] = self.get_selects(form)
			frm['text_areas'] = self.get_text_areas(form)
			
			forms.append(frm)

		self.forms = forms

		return forms

class Links:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.links = []
		self.tag_name = 'link'

	def extract(self):
		page_links = self.page.findAll(name='link')
		links = []

		for link in page_links:
			lnk = {}
			
			_as = link.get('as')
			_crossorigin = link.get('crossorigin')
			_disabled = True if link.get('disabled') else False
			_rel = link.get('rel')
			_href = link.get('href')
			_sizes = link.get('sizes')
			_type = link.get('type')
			_title = link.get('title')
			
			if not (_href):
				continue

			lnk['as'] = _as
			lnk['crossorigin'] = _crossorigin if _crossorigin != ''  else True if _crossorigin else False
			lnk['disabled'] = _disabled
			lnk['rel'] = _rel
			lnk['href'] = _href
			lnk['sizes'] = _sizes
			lnk['type'] = _type
			lnk['title'] = _title

			links.append(lnk)

		self.links = links
		return links

class Anchors:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.anchors = []
		self.tag_name = 'a'

	def extract(self):
		page_anchors = self.page.findAll(name='a')
		anchors = []

		for anchor in page_anchors:
			anchr = {}

			_href = anchor.get('href')
			_type = anchor.get('type')
			_download = anchor.get('download')
			_ping = anchor.get('ping')
			_rel = anchor.get('rel')
			_text = anchor.text.strip()
			_hash = hashlib.md5(_text.encode()).hexdigest()

			if not (_href or _type or _download or _ping or _type or _rel):
				continue

			anchr['href'] = _href
			anchr['download'] = _download if _download != ''  else (True if _download else False)
			anchr['ping'] = _ping
			anchr['rel'] = _rel
			anchr['type'] = _type
			anchr['text'] = _text
			anchr['hash'] = _hash

			anchors.append(anchr)

		self.anchors = anchors
		return anchors

class Areas:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.areas = []
		self.tag_name = 'area'

	def extract(self):
		page_areas = self.page.findAll(name='area')
		areas = []

		for area in page_areas:
			_area_ = {}

			_alt = area.get('alt')
			_download = area.get('download')
			_href = area.get('href')
			_rel = area.get('rel')
			_ping = area.get('ping')

			if not (_href or _rel or _ping):
				continue

			_area_['alt'] = _alt
			_area_['download'] = _download if _download != ''  else True if _download else False
			_area_['href'] = _href
			_area_['rel'] = _rel
			_area_['ping'] = _ping

			areas.append(_area_)

		self.areas = areas
		return areas

class Metas:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.metas = []
		self.tag_name = 'meta'

	def extract(self):
		page_metas = self.page.findAll(name='meta')
		metas = []

		for meta in page_metas:
			_meta_ = {}

			_meta_['charset'] = meta.get('charset')
			
			#does a meta tag have a download attribute?
			_download = meta.get('download')
			
			_meta_['download'] = _download if _download != ''  else (True if _download else False)
			
			_meta_['name'] = meta.get('name')

			_meta_['content'] = meta.get('content')

			_meta_['http-equiv'] = meta.get('http-equiv')

			metas.append(_meta_)

		self.metas = metas
		return metas

class Scripts:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.scripts = []
		self.tag_name = 'script'

	def extract(self):
		page_scripts = self.page.findAll(name='script')
		scripts = []

		for script in page_scripts:
			_script_ = {}

			_src = script.get('src')
			_type = script.get('type')
			_text = script.text.strip()
			_hash = hashlib.md5(_text.encode()).hexdigest()

			_script_['src'] = _src
			
			_script_['type'] = _type

			_script_['hash'] = _hash

			_script_['external'] = True if _src else False

			scripts.append(_script_)

		self.scripts = scripts
		return scripts

class Images:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""

		self.page = page
		self.images = []
		self.tag_name = 'img'

	def extract(self):

		page_images = self.page.findAll(name='img')
		images = []

		for image in page_images:
			_image_ = {}

			_alt = image.get('alt')
			_crossorigin = image.get('crossorigin')
			_src = image.get('src')
			_srcset = image.get('srcset')

			if not (_src or _srcset):
				continue

			_image_['alt'] = _alt
			_image_['crossorigin'] = _crossorigin
			_image_['src'] = _src

			_srcset_ = []

			if _srcset:
				_srcset = _srcset.split(',')
				for _srcst in _srcset:
					url = _srcst.strip().split(' ', 1)[0].strip()
					if url and not url in _srcset_:
						_srcset_.append(url)

			_srcset = _srcset_
			_image_['srcset'] = _srcset

			images.append(_image_)

		self.images = images
		return images

class Media:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.medias = []

	def get_tracks(self, media):
		page_tracks = media.findAll(name='track')
		tracks = []

		for track in page_tracks:
			__track__ = {}
			
			_src = track.get('src')
			_kind = track.get('kind')
			_label = track.get('label')
			_srclang = track.get('srclang')

			if not (_src):
				continue

			__track__['src'] = _src
			__track__['kind'] = _kind
			__track__['label'] = _label
			__track__['srclang'] = _srclang
			
			tracks.append(__track__)

		return tracks

	def get_sources(self, media):
		page_sources = media.findAll(name='source')
		sources = []

		for source in page_sources:
			__source__ = {}
			
			_src = source.get('src')
			_srcset = source.get('srcset')
			_type = source.get('type')
			
			if not (_src or _srcset):
				continue

			__source__['src'] = _src
			__source__['type'] = _type

			_srcset_ = []

			if _srcset:
				_srcset = _srcset.split(',')
				for _srcst in _srcset:
					url = _srcst.strip().split(' ', 1)[0].strip()
					if not url in _srcset_:
						_srcset_.append(url)

			_srcset = _srcset_
			__source__['srcset'] = _srcset

			sources.append(__source__)

		return sources

class Videos(Media):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tag_name = 'video'
	
	def extract(self):

		page_videos = self.page.findAll(name='video')
		videos = []

		for video in page_videos:
			__video__ = {}

			_poster = video.get('poster')
			_src = video.get('src')
			_text = video.text.strip()
			_hash  = hashlib.md5(_text.encode()).hexdigest()
			_sources = self.get_sources(video)
			_tracks = self.get_tracks(video)


			__video__['hash'] = _hash
			__video__['text'] = _text
			__video__['poster'] = _poster
			__video__['src'] = _src
			__video__['sources'] = _sources
			__video__['tracks'] = _tracks

			videos.append(__video__)

		self.medias = videos
		return videos

class Audios(Media):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tag_name = 'audio'
	
	def extract(self):

		page_audios = self.page.findAll(name='audio')
		audios = []

		for audio in page_audios:
			__audio__ = {}

			_poster = audio.get('poster')
			_src = audio.get('src')
			_sources = self.get_sources(audio)
			_text = audio.text.strip()
			_hash  = hashlib.md5(_text.encode()).hexdigest()
			_tracks = self.get_tracks(audio)

			__audio__['hash'] = _hash
			__audio__['text'] = _text
			__audio__['poster'] = _poster
			__audio__['src'] = _src
			__audio__['sources'] = _sources
			__audio__['tracks'] = _tracks

			audios.append(__audio__)
		
		self.medias = audios
		return audios

class IFrames:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.iframes = []
		self.tag_name = 'iframe'

	def extract(self):

		page_iframes = self.page.findAll(name='iframe')
		iframes = []

		for iframe in page_iframes:
			__iframe__ = {}

			_allow = iframe.get('allow')
			_csp = iframe.get('csp')
			_name = iframe.get('name')
			_sandbox = iframe.get('sandbox')
			_src = iframe.get('src')
			_srcdoc = iframe.get('srcdoc')

			__iframe__['allow'] = _allow
			__iframe__['csp'] = _csp
			__iframe__['name'] = _name
			__iframe__['sandbox'] = _sandbox
			__iframe__['src'] = _src
			__iframe__['srcdoc'] = _srcdoc
			
			iframes.append(__iframe__)

		self.iframes = iframes
		return iframes

class Objects:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""

		self.page = page
		self.objects = []
		self.tag_name = 'object'

	def extract(self):

		page_objects = self.page.findAll(name='object')
		objects = []

		for obj in page_objects:
			__object__ = {}


			_archive = obj.get('archive')
			_classid = obj.get('classid')
			_codebase = obj.get('codebase')
			_codetype = obj.get('codetype')
			_data = obj.get('data')
			_name = obj.get('name')
			_type = obj.get('type')


			__object__['archive'] = _archive
			__object__['classid'] = _classid
			__object__['codebase'] = _codebase
			__object__['codetype'] = _codetype
			__object__['data'] = _data
			__object__['name'] = _name
			__object__['type'] = _type
			
			objects.append(__object__)

		self.objects = objects
		return objects

class Embeds:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""

		self.page = page
		self.embeds = []
		self.tag_name = 'embed'

	def extract(self):
		page_embeds = self.page.findAll(name='embed')
		embeds = []

		for embed in page_embeds:
			__embed__ = {}

			_src = embed.get('src')
			_type = embed.get('type')
			
			__embed__['src'] = _src
			__embed__['type'] = _type
			
			embeds.append(__embed__)

		self.embeds = embeds
		return embeds

class SVGs:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.svgs = []
		self.tag_name = 'svg'

	def extract(self):
		page_svgs = self.page.findAll(name='svg')
		svgs = []
		
		for svg in page_svgs:
			__svg__ = {}

			_width = svg.get('width')
			_height = svg.get('height')
			_viewbox = svg.get('viewbox')
			_text = svg.text.strip()
			_hash  = hashlib.md5(_text.encode()).hexdigest()
			_version = svg.get('version')

			__svg__['hash'] = _hash
			__svg__['text'] = _text
			__svg__['width'] = _width
			__svg__['height'] = _height
			__svg__['viewbox'] = _viewbox
			__svg__['version'] = _version

			svgs.append(__svg__)

		self.svgs = svgs
		return svgs

class Styles:
	def __init__(self, page):
		
		"""
		@param page: a `bs4.BeautifulSoup` object containing the html page.
		@type page: bs4.BeautifulSoup
		"""
		
		self.page = page
		self.styles = []
		self.tag_name = 'style'

	def extract(self):
		page_styles = self.page.findAll(name='style')
		styles = []

		for style in page_styles:
			__style__ = {}

			_text = style.text
			_hash = hashlib.md5(_text.encode()).hexdigest()

			__style__['hash'] = _hash

			styles.append(__style__)

		self.styles = styles
		return styles
		
def get_icons(page):
	
	tag_name = 'icon'

	icons = page.findAll(name='link', attrs={'rel':'icon'})
	apple_icons = page.findAll(name='link', attrs={'rel':'apple-touch-icon'})
	
	icons.extend(apple_icons)
	
	apple_icons = page.findAll(name='link', attrs={'rel':'apple-touch-startup-image'})
	icons.extend(apple_icons)
	
	#verify the rel attribute.
	apple_icons = page.findAll(name='link', attrs={'rel':'apple-touch-precomposed'})
	icons.extend(apple_icons)
	
	icons_urls = []

	for icon in icons:
		url = icon.get('href')
		if url and not url in icons_urls:
			_hash = hashlib.md5(url.encode()).hexdigest()
			icons_urls.append({'url':url, 'hash':_hash})

	return tag_name, icons_urls

def get_title(page):
	
	tag_name = 'title'
	title = page.find(name=tag_name)
	_title = {}
	
	if title:
		_text = title.text.strip()
		_title['text'] = _text
		_title['hash'] = hashlib.md5(_text.encode()).hexdigest()
	
	return tag_name, _title

def get_comments(page):
	comments = page.findAll(text=lambda text:isinstance(text, Comment))
	_comments = []

	for comment in comments:
		if comment.strip():
			_comments.append(comment.extract())

	return _comments


def convert_page(html):
	b = BeautifulSoup(html, features='html.parser')
	return b

def process_page(handle):
	b = BeautifulSoup(handle.read(), features='html.parser')
	
	tags_mapping = {}
	attrs_mapping = {}

	tags = b.select('html *')
	
	for tag in tags:
		tag_name = tag.name
		
		if tag_name in tags_mapping:
			tags_mapping[tag_name] = tags_mapping.get(tag_name) + 1
		else:
			tags_mapping[tag_name] = 1

		tag_attrs = tag.attrs
		for attr_name in tag_attrs:
			if attr_name in attrs_mapping:
				attrs_mapping[attr_name] = attrs_mapping.get(attr_name) + 1
			else:
				attrs_mapping[attr_name] = 1

	print(tags_mapping)
	print(attrs_mapping)

def get_base(page):
	
	tag_name = 'base'

	base = page.find(name=tag_name)

	_base = {}

	if base:
		_url = base.get('url', '')
		_hash = hashlib.md5(_url.encode()).hexdigest()

		_base['url'] = _url
		_base['hash'] = _hash

	return tag_name, _base

def get_page_info(page):
	tag_name, t = get_title(page)
	page_title = t.get('title', '')
	page_hash = t.get('hash', '')
	return (page_title, page_hash)

def parse_data(data, name=""):
	
	values = []

	if type(data) == dict:
		for k in data:

			v = data[k]
			n = name + '.' + str(k)
			r = parse_data(v, n)
			
			if type(r) == list:
				values.extend(r)
			else:
				vv = (n, r)
				values.append(vv)

		return values

	elif type(data) == list:
		n = name
		
		if len(n) > 2 and n[-1].lower() == 's':
			n = n.rstrip('s')

		for item in data:
			r = parse_data(item, n)

			if type(r) == list:
				values.extend(r)
			else:
				vv = (n, r)
				values.append(vv)

		return values
	
	elif data == None:
		return None

	else:
		return str(data)

