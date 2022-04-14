import json
import pprint

from .classes.pages.controller import Controller
from .classes.pages.ScrapeIt import Scraper

"""
TODO:
1) accept/reject a response based on its content-type.
2) create handlers for each content type.
3)
"""

# controller = Controller()

# allowed_domains = ['hyperpure.com', 'www.hyperpure.com']
# allowed_domains = ['casper.com']
# allowed_domains = ['localhost']
# allowed_hosts = []

# controller.add_urls(['http://localhost'])

# controller.set_program_option('include_domain', allowed_domains)
# controller.set_program_option('include_host', allowed_hosts)

# scraper = Scraper(controller)
# scraper.max_bots_size = 6
# scraper.verbosity = 4

# output = './storage/links-casper.com.json'

# scraper.set_output(0, './storage/links-400-localhost.json')

# # scraper.set_output_file(output)

# try:
# 	scraper.start()
# 	# pprint.pprint(scraper.get_info())
# 	print(len(scraper.get_info()['processed_links']))

# except Exception as e:
# 	raise e

# def get_pages(allowed_domains)