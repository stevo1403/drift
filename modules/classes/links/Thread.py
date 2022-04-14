import grequests
from gevent import Greenlet, time


class Bot(Greenlet):

	def __init__(self, controller):

		self.controller = controller

		self.stop_running = False

		self.urls = []

		#stream response(process the response on-demand.)
		self.USE_RESPONSE_STREAMING = True

		self.REQUESTS_PER_SECOND = 2

		self.verbosity = 3

		super().__init__()

	def _run(self):
		self.run_tasks()

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name
		return self.name

	def print_exception(self, message):
		if self.verbosity > 0:
			print(message)

	def print_info(self, message):
		if self.verbosity >= 4:
			print(message)

	def print_exception(self, message):
		if self.verbosity > 0:
			print(message)

	def print_info(self, message):
		if self.verbosity >= 4:
			print(message)

	def change_status(self, status=0):
		"""
		Changes the thread status to `status`.
		@param status: the status to change to
		@type status: int
		@rtype: int
		"""
		name = int(self.name)
		self.controller.thread_status[name] = status
		return status

	def run_tasks(self):

		self.greenlet_state = 'STARTED'

		try:
			self.process_tasks()
		except Exception as e:
			print('Exception: ', e)
			# self.log_exception(e, 'critical', 'Error occurred while running greenlet tasks')
		
		self.greenlet_state = 'ENDED'

	def response_hook(self, response, *args, **kwargs):
		#handle redirects and incomplete response.
		pass

	def handle_exception(self, request, exception):
		#handle request exception
		self.print_exception("[+] An exception occurred while sending request: %s"%(exception))
		self.print_exception('')

	def process_tasks(self):
		
		"""
		Grabs urls from the queue and process it.
		"""

		print('[~] Bot-%s is starting.'%(self.getName()))

		#tells the controller that the thread is active.
		self.controller.set_thread_state(self.getName(), 1)
		
		print()

		time.sleep(2)

		self.urls = self.controller.get_urls()
		
		NUM_SESSIONS = 5
		sessions  = []

		timeout = self.controller.get_request_timeout()

		for i in range(NUM_SESSIONS):
			
			session = self.controller.create_session()
			session.headers.update(self.controller.get_request_headers())

			sessions.append(session)

		hooks = {'response':self.response_hook}

		while True:
			
			if not self.urls:
				self.controller.register_event(self.getName(), 'NO_URLS')
			else:
				self.controller.delete_event(self.getName(), 'NO_URLS')

			bots_size = self.controller.get_bots_size()

			if len(self.controller.get_event_ids('NO_URLS')) == bots_size:
				break

			pending_requests = []
			
			time.sleep(2)

			for index, url in enumerate(self.urls):
				session = sessions[index % NUM_SESSIONS]

				request = grequests.get(
					url, hooks=hooks,
					session=session, timeout= timeout
					)

				pending_requests.append(request)

			if pending_requests:

				responses = grequests.imap(
					pending_requests, stream=self.USE_RESPONSE_STREAMING, size=self.REQUESTS_PER_SECOND,
					exception_handler=self.handle_exception
					)
				
				for response in responses:
					self.controller.process_response(response)

			
			#get more urls
			self.urls = self.controller.get_urls()
			
		print('[~] Bot-%s has returned.'%(self.getName()))

		#tells the controller that the thread is not active.
		self.controller.set_thread_state(self.getName(), 0)
