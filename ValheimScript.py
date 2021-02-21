# Run this script using Python 3
# Fill in global values to match your server ip, port, and credentials
# SAVE_GAME_NAME is the name of your save world in Valheim
# LOCAL_DIRECTORY is the name you would like to use for your local backup folder
# If this script is located at 'C:\Users\temp\Documents\Valheim-Backup\ValheimScript.py', then
# backups will be stored in 'C:\Users\temp\Documents\Valheim-Backup\ValheimBackups'
# BACKUP_TIME_SECONDS is the number of seconds between backups (default 600s = 10 mins)

# TODO: read variables from config file
#

import os
import time
import shutil
import urllib.request as request
from contextlib import closing

USERNAME = ''
PASSWORD = ''
SERVER_IP = ''
SERVER_PORT = ''
SAVE_GAME_NAME = ''
LOCAL_DIRECTORY = 'ValheimBackups'
BACKUP_TIME_SECONDS = 600

def main():
    # If the local backup directory does not exist yet, create it
    if not os.path.exists(LOCAL_DIRECTORY):
        os.makedirs(LOCAL_DIRECTORY)

    # Loop until the user stops script
    while True:

        # Grab the db world file
        retrieve_file('db')

        # Grab the fwl world file
        retrieve_file('fwl')

        # How often you want the backup to run
        time.sleep(BACKUP_TIME_SECONDS)

# Function to retrieve file from FTP server with username and password credentials
def retrieve_file(file_type):
    with closing(request.urlopen('ftp://{}:{}@{}:{}/save/worlds/{}.{}'.format(USERNAME, PASSWORD, SERVER_IP, SERVER_PORT, SAVE_GAME_NAME, file_type))) as r:
        with open('{}/{}.{}'.format(LOCAL_DIRECTORY, SAVE_GAME_NAME, file_type), 'wb') as f:
            shutil.copyfileobj(r, f)

if __name__ == "__main__":
    # execute only if run as a script
    main()
