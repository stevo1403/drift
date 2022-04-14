from drift.tables import Program as ProgramTable


class Program:

	def __init__(self, program_id, program_name, program_url,
	 program_handle, disclosure_url, disclosure_email, 
	 offers_rewards, offers_thanks, internet_bug_bounty, team_type):

		self.program_id = program_id or -1

		self.program_name = program_name or ''

		self.program_url = program_url or ''

		self.program_handle = program_handle or ''

		self.disclosure_url = disclosure_url or ''

		self.disclosure_email = disclosure_email or ''

		self.offers_rewards = bool(offers_rewards)

		self.offers_thanks = bool(offers_thanks)

		self.internet_bug_bounty = bool(internet_bug_bounty)

		self.team_type = team_type

	def get_program_id(self):
		return self.program_id

	def set_program_id(self, program_id):
		self.program_id = program_id or -1
		return self

	def get_program_name(self):
		return self.program_name.lower()

	def set_program_name(self, program_name):
		self.program_name = program_name.lower()
		return self

	def get_program_url(self):
		return self.program_url

	def set_program_url(self, program_url):
		self.program_url = program_url
		return self

	def get_program_handle(self):
		return self.program_handle.lower()

	def set_program_handle(self, program_handle):
		self.program_handle = program_handle.lower()
		return self

	def get_disclosure_email(self):
		return self.disclosure_email.lower()

	def set_disclosure_email(self, disclosure_email):
		self.disclosure_email = disclosure_email.lower()
		return self

	def get_disclosure_url(self):
		return self.disclosure_url

	def set_disclosure_url(self, disclosure_url):
		self.disclosure_url = disclosure_url
		return self

	def get_offers_thanks(self):
		return self.offers_thanks

	def set_offers_thanks(self, offers_thanks):
		self.offers_thanks = offers_thanks
		return self

	def get_offers_rewards(self):
		return self.offers_rewards

	def set_offers_rewards(self, offers_rewards):
		self.offers_rewards = offers_rewards
		return self

	def get_internet_bug_bounty(self):
		return self.internet_bug_bounty

	def set_internet_bug_bounty(self, internet_bug_bounty):
		self.internet_bug_bounty = internet_bug_bounty
		return self

	def get_team_type(self):
		return self.team_type.lower()

	def set_team_type(self, team_type):
		self.team_type = team_type.lower()
		return self

	def create_record(self):
		return ProgramTable(
			program_id=self.get_program_id(), program_name=self.get_program_name(), program_url=self.get_program_url(),
			program_handle=self.get_program_handle(), disclosure_url=self.get_disclosure_url(), disclosure_email=self.get_disclosure_email(),
			offers_rewards=self.get_offers_rewards(), offers_thanks=self.get_offers_thanks(), internet_bug_bounty=self.get_internet_bug_bounty(),
			team_type=self.get_team_type()
			)