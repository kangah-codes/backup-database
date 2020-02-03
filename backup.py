# backup mongodb every 24hrs

import os
import logging
import datetime
from urllib.parse import urlparse
import subprocess
import slack

client = slack.WebClient(token='xoxb-919881679474-922523632689-avtN5jmEihuoieHdIRd0cb02')

# setting a log file to log all data
logging.basicConfig(level=logging.INFO)

def backup(url):
	database_url = urlparse(url)

	# check if the database is a mongo database url
	assert database_url.scheme == 'mongodb', "URL must be MongoDB URL"

	location = database_url.netloc
	username = database_url.username
	password = database_url.password
	hostname = database_url.hostname
	port = database_url.port
	db = database_url.path[1:]

	logging.info(f"Parsed database url at {datetime.datetime.now()}")

	# set an output directory for the database
	# output_file = os.path.abspath(os.path.join(os.path.curdir, '/'))
	output_file = f'{os.getcwd()}/backup'

	assert os.path.isdir(output_file), 'Directory does not exist'

	#use subprocess to execute shell command to backup database
	os.system(f"mongodump -host {hostname} -u {username} -p {password} -d {db} --port {port} -o {output_file}")

	# log the output of the command
	logging.info(f"Backed up database at {datetime.datetime.now()}")
	response = client.files_upload(
		channels="#backups",
		file=f"{os.getcwd()}/backup"
	)

	assert response['ok'], "Could not send file"

	logging.info(f"Sent backup to slack channel at {datetime.datetime.now()}")



if __name__ == '__main__':
	try:
		backup('mongodb://heroku_dczdt2sx:ifhpheh6mkgeh9affb2ttftn52@ds147446.mlab.com:47446/heroku_dczdt2sx')
		#backup('postgres://postgres:ilovekwame1@127.0.0.1:5432/medic_mall')
	except AssertionError as e:
		logging.error(e)