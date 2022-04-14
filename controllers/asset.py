from drift.tables import Asset as AssetTable


class Asset:

	def __init__(self, asset_id, asset_identifier, asset_type, 
		rendered_instruction, max_severity, eligible_for_bounty, in_scope):

		self.asset_id = asset_id or ''

		self.asset_identifier = asset_identifier or []

		self.asset_type = asset_type or ''

		self.rendered_instruction = rendered_instruction or ''

		self.max_severity = max_severity or ''

		self.eligible_for_bounty = bool(eligible_for_bounty)

		self.in_scope = bool(in_scope)

	def get_asset_id(self):
		return self.asset_id

	def set_asset_id(self, asset_id):
		self.asset_id = asset_id or -1
		return self

	def get_asset_identifier(self):
		return self.asset_identifier

	def set_asset_identifier(self, asset_identifier):
		self.asset_identifier = asset_identifier
		return self

	def get_asset_type(self):
		return self.asset_type

	def set_asset_type(self, asset_type):
		self.asset_type = asset_type
		return self

	def get_rendered_instruction(self):
		return self.rendered_instruction

	def set_rendered_instruction(self, rendered_instruction):
		self.rendered_instruction = rendered_instruction
		return self

	def get_max_severity(self):
		return self.max_severity

	def set_max_severity(self, max_severity):
		self.max_severity = max_severity
		return self

	def get_eligible_for_bounty(self):
		return self.eligible_for_bounty

	def set_eligible_for_bounty(self, eligible_for_bounty):
		self.eligible_for_bounty = eligible_for_bounty
		return self

	def get_in_sope(self):
		return self.in_sope

	def set_in_sope(self, in_sope):
		self.in_sope = eligible_for_bounty
		return self

	def create_record(self):
		return AssetTable(
			asset_id=self.get_asset_id(), asset_identifier=self.get_asset_identifier(), 
			asset_type=self.get_asset_type(), rendered_instruction=self.get_rendered_instruction(), 
			eligible_for_bounty=self.get_eligible_for_bounty(), max_severity=self.get_max_severity(),
			in_sope=self.get_in_sope()
			)