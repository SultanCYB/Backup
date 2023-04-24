#!/usr/bin/env python3
'''
Simple program for backup
'''
import shutil  # for copying the files and folders to the backup path
import sys  # for exiting after error or the backup is done

from pathlib import Path  # makes working with paths easier
from os import listdir  # makes working with paths easier

from datetime import date  # to decide if it's time to backu[]
from plyer import notification  # for sending alerts regarding errors or info about backup

#########################################################
# variables declartions and more at the end of the file #
#########################################################


def alerts(number):
    '''Alert function that sending notifications to your PC 
    concerning what happens while the program is running

    Ref codes manual :
      [-1] log file reading error
      [0] backup error
      [0.5] log file writing error
      [1] start backup
      [2] backup done'''

    if number == -1:
        return notification.notify("Backup", f"Log file reading error\nError : {number}", "Backup")

    elif number == 0:
        return notification.notify(
            "Backup", f"Error occured couldn't backup\nError : {number}", "Backup"
        )

    elif number == 0.5:
        return notification.notify("Backup", f"Log file writting error\nError : {number}", "Backup")

    elif number == 1:

        return notification.notify(
            "Backup", f"Backing up..\nlast backup : {days_diff} days ago", "Backup"
        )

    elif number == 2:
        return notification.notify("Backup", "Backup done", "Backup")


def to_ignore(path, names):
    '''Function that returns a list of folders and files you don't want to backup
    You need this function if there are files and folders in the path you want to backup, that you don't 
    want to backup them.

    If you don't then just keep it as it is'''

    folders = []

    return folders


def backup():

    try:
        alerts(1)  # Starting the backup process

        for i in paths_src:

            shutil.copytree(src=i, dst=path_dest, ignore=to_ignore, dirs_exist_ok=True)

        else:
            file_operations('w')
            # calling the function to start writing the new date because the backup is done

    except:
        alerts(0)  # sending an alert regarding that there is a backup error
        sys.exit()


def file_operations(operation):
    ''' file operations function that read from and write to the log file'''

    global days_diff  # globaling this variable so we can use it in the alerts function

    if operation == 'r':  # if it was a read operation

        try:
            with open(log_file_path, operation) as file:
                file = file.read().split("-")

                file = list(map(int, file))  # converting the year, month, day to int

                year, month, day = file[0], file[1], file[2]

                last_date = date(year, month, day)  # converting it to delta object

                days_diff = (current - last_date).days  # getting the days difference

                if days_diff >= limit:  # comparing if the difference equal to or bigger than the limit
                    return backup()

                else:
                    sys.exit()

        except:

            alerts(-1)  # there was a log file reading error

            sys.exit()

    elif operation == 'w':

        try:
            with open(log_file_path, 'w') as file:
                file.write(str(current))  # writting the new date to the log file

                # converting current to str because it is still a delta object

            alerts(2)  # sending an alert regarding that the backup is done

        except:
            alerts(0.5)  # sending an alert regarding that there is a log file error
            sys.exit()


# Global variables :

# Things you can change

# --------------------------------------------------------------------

paths_src = Path(data_you_want_to_backup)  # The path you want to backup, You must deteremine it

paths_src = list(paths_src)  # converting the map object to a list object

path_dest = Path(destination_of_backup)  # The destination of the backup, You must deteremine it

log_file_path = Path(the_path_of_the_log_file)  # log file path, You must deteremine it

limit = 7  # The default days to backup again is 7, You can change it

#-------------------------------------------------------------------------------

# Things you mustn't change

# --------------------------------------------------------------------

current = date.today()  # Getting today date

# Program start

file_operations('r')  # Calling the function to read the log file

# --------------------------------------------------------------------
''' 

Log file format :

 YYYY-MM-DD

Log file name :

 Your choice, a .txt file, or a .log file

Log file path :

 Your choice

You mustn't edit the file contents or name to keep the program running normally

I'm not responsible for any data loss.

'''