# backup mongodb every 24hrs

import os
import logging
import datetime
from urllib.parse import urlparse
import subprocess
import slackclient

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
	output_dir = os.path.abspath(os.path.join(os.path.curdir, '/'))

	assert os.path.isdir(output_dir), 'Directory does not exist'

	# use subprocess to execute shell command to backup database
	execute_backup = subprocess.check_output([
		'mongodump',
		'-host', f'{hostname}',
		'-u', f'{username}',
		'-p', f'{password}',
		'-d', f'{db}',
		'--port', f'{port}',
		'-o', f'{output_dir}'
	])

	# log the output of the command
	logging.info(f"Backed up database at {datetime.datetime.now()}")
	logging.info(execute_backup)

	# set a filename to call the zipped file
	zipped_name = f"{datetime.datetime.now()}.zip"

	# zip the database backup

	execute_command = subprocess.call([
		'zip',
		'-j',
		zipped_name,
		f'{output_dir}',
		# move the zipped file to root directory
		# so that we can retrieve it easily
		'cd',
		'/'
	])

	logging.info(f"Zipped output directory into {zipped_name}")

	response = client.files_upload(
		channels="#backups",
		file=f"/{zipped_name}"
	)

	assert response['ok'], "Could not send file"

	logging.info(f"Sent backup to slack channel at {datetime.datetime.now()}")



if __name__ == '__main__':
	try:
		backup('mongodb://heroku_dczdt2sx:ifhpheh6mkgeh9affb2ttftn52@ds147446.mlab.com:47446/heroku_dczdt2sx')
	except AssertionError as e:
		logging.error(e)