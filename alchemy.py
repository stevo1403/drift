import time
from urllib.parse import urlencode

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from . import db_config

query_params = {'charset':'utf8mb4'}
query_params = urlencode(query_params)

from .tables import Base, Hostname

if query_params:
	query_params = "?" + query_params
else:
	query_params = ""


engine = sqlalchemy.create_engine(
	'mysql+pymysql://%s:%s@%s/%s?%s'%(db_config.db_username, db_config.db_password, 
		db_config.db_host, db_config.db_name, query_params
		)
	)

Session = sessionmaker(bind=engine)

def delete_tables(checkfirst=True):

	session = Session()
	Base.metadata.drop_all(engine, Base.metadata.tables.values(), checkfirst=checkfirst)
	session.flush()
	session.commit()
	session.close()

def create_tables(checkfirst=True):
	session = Session()
	Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=checkfirst)
	session.flush()
	session.commit()
	session.close()
	
def insert_time(record):
	record.snapshot_time = time.time()
	t = time.gmtime()
	record.snapshot_year = t.tm_year
	record.snapshot_month = t.tm_mon
	record.snapshot_day = t.tm_mday
	return record
