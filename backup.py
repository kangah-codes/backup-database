# backup mongodb every 24hrs

import os
import logging
import datetime
from urllib.parse import urlparse
import subprocess
import slack

client = slack.WebClient(token='yourSlackToken')

# setting a log file to log all data
logging.basicConfig(filename='backup.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

	logging.info("Parsed database url")

	# set an output directory for the database
	output_file = f'{os.getcwd()}/backup'

	# assert os.path.isdir(output_file), 'Directory does not exist'

	#use subprocess to execute shell command to backup database
	os.system(f"mongodump --host {hostname} -u {username} -p {password} -d {db} --port {port} -o {output_file}")
	
	# compress the backup directory
	zip_name = datetime.datetime.now().today()
	
	os.system(f"zip -r {str(zip_name).split(' ')[0]} backup/heroku_dczdt2sx")
	
	logging.info("Compressed database backup")

	# log the output of the command
	logging.info(f"Backed up database at {datetime.datetime.now()}")
	response = client.files_upload(
		channels="#backups",
		file=f"{os.getcwd()}/{str(zip_name).split(' ')[0]}.zip"
	)

	assert response['ok'], "Could not send file"

	logging.info("Sent backup to slack channel")
		  
	os.system(f"rm {str(zip_name).split(' ')[0]}.zip")
		  
	logging.info("Removed zip file")



if __name__ == '__main__':
	try:
		backup('your_DB_URI')
	except AssertionError as e:
		logging.error(e)
