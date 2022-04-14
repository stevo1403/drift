from drift import alchemy
from drift.alchemy import Session, create_tables, delete_tables, insert_time
from drift.controllers.hostname import Hostname
from drift.controllers.program import Program

json_file = 'h1/hackerone-bb-programs.json'

import json

keys = set()

session = Session()

delete_tables()
create_tables()

with open(json_file) as j:
	programs = json.load(j)['results']
	for program in programs:

		id = program.get('id')
		name = program.get('name')
		url = program.get('url')
		handle = program.get('handle')
		disclosure_email = program.get('disclosure_email')
		disclosure_url = program.get('disclosure_url')
		offers_rewards = program.get('offers_rewards')
		offers_thanks = program.get('offers_thanks')
		internet_bug_bounty = program.get('internet_bug_bounty')
		team_type = program.get('team_type')

		p = Program(program_id=id, program_name=name, program_url=url, program_handle=handle, 
			disclosure_email=disclosure_email, disclosure_url=disclosure_url, offers_rewards=offers_rewards,
			offers_thanks=offers_thanks, internet_bug_bounty=internet_bug_bounty, team_type=team_type
		 )

		record = p.create_record()
		insert_time(record)
		session.add(record)
		
		session.flush()
		session.commit()

		keys.update(program.keys())
		# print(program.keys())

session.close()
print(sorted(keys))