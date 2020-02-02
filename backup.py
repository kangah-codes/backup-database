# backup mongodb every 24hrs

import os
import logging
import datetime
from urllib.parse import urlparse
import subprocess

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
	logging.info(execute_backup)

if __name__ == '__main__':
	try:
		backup('mongodb://heroku_dczdt2sx:ifhpheh6mkgeh9affb2ttftn52@ds147446.mlab.com:47446/heroku_dczdt2sx')
	except AssertionError as e:
		logging.error(e)