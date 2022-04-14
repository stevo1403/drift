import json
import pprint

from .classes.links.controller import Controller
from .classes.links.ScrapeIt import Scraper

"""
TODO:
1) accept/reject a response based on its content-type.
2) create handlers for each content type.
3)
"""
# controller = Controller()

# allowed_domains = ['hyperpure.com', 'www.hyperpure.com']
# allowed_hosts = []

# controller.add_urls(['https://hyperpure.com'])

# controller.set_program_option('include_domain', allowed_domains)
# controller.set_program_option('include_host', allowed_hosts)

# scraper = Scraper(controller)

# scraper.max_bots_size = 6
# scraper.verbosity = 4

# try:
# 	scraper.start()
# 	pprint.pprint(scraper.get_info())
# 	print(len(scraper.get_info()['processed_links']))

# except Exception as e:
# 	raise e