import hashlib
import json
import os

import requests
from bs4 import BeautifulSoup
from helpers.pages import (Anchors, Areas, Audios, Embeds, Forms, IFrames,
                           Images, Links, Metas, Objects, Scripts, Styles,
                           SVGs, Videos, convert_page, get_base, get_comments,
                           get_icons, get_title, parse_data)

user_agent = "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"

filename = "../../store/twitter-homepage.html"

headers = {'User-Agent':user_agent, 'Accept':'text/html'}

class Selectors:
	PAGE_TITLE = 'meta'


def download_page(url, headers={}):
	with requests.get(url, headers=headers, timeout=15) as response:
		return response.text

def save_page(content, page_name):
	with open(page_name, 'wt', encoding='utf-8') as f:
		f.write(content)

	return page_name

sections = {
	'e-commerce':[
		'amazon.com',
		'ebay.com',
		'alibaba.com',
		'overstock.com',
	],
	'image-hosting':[
		'imgur.com',
		'flickr.com',
		'dreamstime.com',
		'instagram.com',
	],
	'social-media':[
		'facebook.com',
		'instagram.com',
		'twitter.com',
		'linkedin.com',
	],
	'e-learning':[
		'khanacademy.com',
		'coursera.com',
		'udemy.com',
		'pluralsight.com'
	],
	'media-distribution':[
		'netflix.com',
		'soundcloud.com',
		'hulu.com',
		'bandcamp.com',
	],
}

filename = open('../../store/page-mozilla.html', 'rt', encoding='utf-8')

def download_pages():

	for section in sections:
		sites = sections[section]
		for site in sites:
			url = 'http://' + site + '/'
			filename = site.split('.',1)[0]
			filename = os.path.join('../../store', 'page-'+filename+'.html')
			print(url, filename)
			try:
				content = download_page(url, headers)
				save_page(content, filename)
			except Exception as e:
				print(e)

def open_page(hostname):
	filename = hostname.split('.',1)[0]
	filename = os.path.join('../../store', 'page-'+filename+'.html')
	f = open(filename, 'rt', encoding='utf-8')
	return f

# hostname = 'amazon.com'
# print(hostname)
# f = open_page(hostname)
# process_page(f)

# exit()


data = {

    "method": "get",
    "text": "Type the characters you see",
    "hash": "746a5a2282377026271dc7e",
    "action": "/errors/validateCaptc",
    "enctype": None,
    "hidden": None,
    "buttons": [
    1,2,3
     # {
     #    "name": "1",
     #    "type": "1",
     #    "value": "1"
     #  },
     #  {
     #    "name": "2",
     #    "type": "2",
     #    "value": "2"
     #  }
    ],

   }



# dd  = parse_data(data, 'form')

# print( json.dumps(dd, indent=2) )

# exit()

html = filename.read()

html = """
<head>
	<link rel="icon apple-touch-icon" href="http://example.com/icon.ico"/>
</head>

<form>
<input name="username" placeholder="Username"></input>
<input name="password" ></input>
<input name="csrf_token" value="simple value"></input>
<button name="submit" type="submit"></button>
<select name="pets" multiple size="4">
<option value="dog">Dog</option>
<option value="hamster">Hamster</option>
<option value="cat" selected>Cat</option>
</select>
</form>
<img srcset="http://example.com/images/img1.png 2w, http://example.com/images/img2.png 2x" class="a b"/>
<video src="http://example.com/video.mp4">
<source src="/media/cc0-videos/flower.webm" type="video/webm" />
</video>
"""

# b = BeautifulSoup(html, features='html.parser')

# imgs = b.findAll('img')
# for img in imgs:
# 	print(img.get('class'))

# exit()

"""
Resource1 => Resource2
rel attribute valid on linlk, a, area, and form element.
"""

for section in sections:

	hostnames = sections[section]
	for hostname in hostnames:
		
		h = open_page(hostname)
		html = h.read()

		print('Loading html.')
		b = BeautifulSoup(html, features='html.parser')

		print('Loaded html.')

		icons = get_icons(b)


		# f = Forms(b)

		# a = Anchors(b)

		# aa = Areas(b)

		# l = Links(b)

		# m = Metas(b)

		# im = Images(b)

		# vi = Videos(b)

		# au = Audios(b)

		# ob = Objects(b)

		# em = Embeds(b)

		# _if = IFrames(b)

		# s = Scripts(b)

		# sv = SVGs(b)

		# st = Styles(b)

		# t = get_title(b)

		# print(icons)
		c = get_comments(b)

		print(c)
		print("=="*10)

		# tag_name = f.tag_name

		# fv = c.extract()
		# dd = parse_data(fv, tag_name)
		
		# print( json.dumps(dd, indent=2) )

		# print( json.dumps(f, indent=2) )

		# break

	# break

exit()
# print( json.dumps(l.extract(), indent=2) )
# print( json.dumps(sv.extract(), indent=2) )

print(t)

# select = b.findAll('select')

# for slt in select:
# 	slt_name = slt.get('name')
# 	print(slt_name)
# 	print(slt.attrs)
# 	options = slt.findAll('option')
# 	for option in options:
# 		print(option.get('value'))

