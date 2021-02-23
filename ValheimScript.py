# Run this script using Python 3
# Fill in global values to match your server ip, port, and credentials
# SAVE_GAME_NAME is the name of your save world in Valheim
# LOCAL_DIRECTORY is the name you would like to use for your local backup folder
# If this script is located at 'C:\Users\temp\Documents\Valheim-Backup\ValheimScript.py', then
# backups will be stored in 'C:\Users\temp\Documents\Valheim-Backup\ValheimBackups'
# BACKUP_TIME_SECONDS is the number of seconds between backups (default 600s = 10 mins)

# TODO: read variables from config file
# TODO: fill out readme

import os
import time
import shutil
from pytz import timezone
from datetime import datetime
from contextlib import closing
import urllib.request as request

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

    count = 0

    # Loop until the user stops script
    while True:
        hour_passed = False

        # After each hour, save off backup with timestamp
        if count == 5:
            hour_passed = True
            count = 0

        retrieve_files(hour_passed)

        count += 1
        print('Backup created: {}'.format(datetime.now(tz)))

        # How often you want the backup to run
        time.sleep(BACKUP_TIME_SECONDS)


def retrieve_files(hour_passed):
    # Grab the db world file
    retrieve_file('db', hour_passed)

    # Grab the fwl world file
    retrieve_file('fwl', hour_passed)


# Function to retrieve file from FTP server with username and password credentials
# We want to keep 2 local backups at a time, plus an additional timestamped save file every hour
def retrieve_file(file_type, hour_passed):
    new_file_path = '{}/{}.{}'.format(LOCAL_DIRECTORY, SAVE_GAME_NAME, file_type)
    old_file_path = '{}/{}_2.{}'.format(LOCAL_DIRECTORY, SAVE_GAME_NAME, file_type)
    ftp_file_path = 'ftp://{}:{}@{}:{}/save/worlds/{}.{}'.format(USERNAME, PASSWORD, SERVER_IP, SERVER_PORT, SAVE_GAME_NAME, file_type)

    # Replace secondary backup
    if os.path.exists(new_file_path):
        with open(new_file_path, 'rb') as new_file:
            with open(old_file_path, 'wb') as old_file:
                shutil.copyfileobj(new_file, old_file)

    # Replace new backup
    with closing(request.urlopen(ftp_file_path)) as server_file:
        with open(new_file_path, 'wb') as new_file:
            shutil.copyfileobj(server_file, new_file)

    # After an hour has passed, we want to create an additional backup with a timestamp so it's not overwritten
    if hour_passed:
        print('One hour passed, saving off new file...')
        with closing(request.urlopen(ftp_file_path)) as server_file:
            new_file_path = '{}/{}.{}'.format(LOCAL_DIRECTORY, SAVE_GAME_NAME + '_{}'.format(datetime.now(tz)), file_type)
            with open(new_file_path, 'wb') as new_timestamp_file:
                shutil.copyfileobj(server_file, new_timestamp_file)


if __name__ == "__main__":
    main()
