#!/usr/bin/env python3
'''
Python tool for regular backup
'''

# for files and paths
import shutil  # for copying the files and folders to the backup path
import os  # makes working with paths easier
import tarfile  # archiving the files
import re  # regex to get the current file path
from typing import List  # for annotations
from io import BytesIO

# for date and notifications
from datetime import date  # to decide if it's time to backup
from plyer import notification  # for sending alerts regarding errors or info

# for errors and else
import sys  # for exiting the program, and to get information of errors
import time  # for working with the error time and get the time the program needed to execute

##################################################################
                #### Check the end of the file ####
##################################################################


def Error_log(error_name, error_time) -> None:
    ''' function to log errors to the error log file '''

    try:
        with open(error_path, 'a') as file:

            file.write(f'[ERROR] [{error_time}] -->  {error_name}\n\n')

            file.write(f'Error type : {type(error_name).__name__}\n')
            file.write(f'Line : {(sys.exc_info()[2]).tb_lineno}\n')

            file.write(f'For additional help, you can contact me at : sultanxx575@gmail.com\n')

            file.write(f"{'-'*65}\n")

    except Exception as e:
        error_time_2 = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # the time of the error
        print(
            f"""The program was trying to write an error to the error log but it seems that another
error appeared in the error log function, so this process has failed. These are the errors :


-    error information of the error that faced the error log function are:      

    error name : {e}
    error time : {error_time_2}
    error line : {(sys.exc_info()[2]).tb_lineno}
    error type : {type(e).__name__}

-    error information for the second error that happend in somewhere that isn't in the error log function are:

    error name : {error_name}
    error time : {error_time}
    error type : {type(error_name).__name__}


    if you keep getting the same problem contact me at

    sultanxx575@gmail.com"""
        )

        sys.exit()


def Alerts(number, days_diff=None, finish=None) -> None:
    '''Alert function that send notifications to your PC 
    concerning the current status of the program, success, error
    '''
    try:

        # error
        if number == -1:
            notification.notify("Backup", "There is an error, Check the error log file", "Backup")

        # status
        elif number == 1:
            notification.notify(
                "Backup", f"Backing up..\nlast backup : {days_diff} days ago", "Backup"
            )

        # success
        elif number == 2:
            notification.notify("Backup", f"Backup done in {finish} seconds", "Backup")

    except Exception as e:
        error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # the time of the error

        Error_log(e, error_time)  # calling the error log function to write to the error log

        if finish:
            print(
                "The backup is done. However, the alert function doesn't work for some reason.. Check the error log"
            )
        else:
            print(
                "The backup has failed. and the alert function doesn't work for some reason.. Check the error log"
            )

        sys.exit()


def Backup(archive_path):
    ''' The backup function '''
    global finish
    try:
        # checking that the path exists.
        if not os.path.exists(archive_path):
            raise IOError("archive directory doesn't exist")

        # Starting the backup process

        archive_path += "backup.tar"

        if not overwrite and os.path.isfile(archive_path):

            i = 1

            archive_path = re.sub(r"\.tar$", "", archive_path, re.IGNORECASE)

            # to also prevent overwritting any other duplicated archives
            while os.path.isfile(f"{archive_path}_{i}.tar"):
                i += 1

            archive_path += f"_{i}.tar"

        with tarfile.open(archive_path, 'w') as my_archive:

            for src in file_sources:  # loop into the given file sources

                if os.path.isfile(src):  # if the given path is a path for a file
                    # to add file sources that has only one file in it is path
                    my_archive.add(src, os.path.basename(src))

                else:

                    for root, dirs, files in os.walk(src):

                        # checking if the ignored files or folders are in the given path
                        for ignored in ignore_path:
                            if ignored in dirs or ignored in root:
                                break

                        # the else here means : if the loop ended without any break
                        else:
                            # looping into the files of the current directory
                            for file in files:

                                # joining the path and the file to get the desired file
                                file_path = os.path.join(root, file)
                                my_archive.add(file_path)

            # simple text file contain date of the backup

            # date, hours, minutes, seconds
            exact_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # creating a stream for bytes
            fake_file = BytesIO()

            # writting the content of the file
            fake_file.write(f"The backup ended successfuly at {exact_time}".encode())

            # the name of the file
            tar_info = tarfile.TarInfo(name=f"Backup date {exact_time}.txt")

            # getting the size of the file
            tar_info.size = fake_file.tell()

            fake_file.seek(0)  # moving the cursor to 0 byte, to read the file again

            my_archive.addfile(
                fileobj=fake_file, tarinfo=tar_info
            )  # adding the file to the archive

        # calling the func to start writing the new date after the backup is done
        finish = round(time.time() - start, 2)

        return 1

    except Exception as e:
        error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # the time of the error

        Error_log(e, error_time)  # calling the error log function to write to the error log
        Alerts(-1)  # there was an error, so alert will be sent
        sys.exit()


def Log_Backup(operation):
    ''' backup log operations function that read from and log to the backup log file'''

    if operation == 'r':  # if it was a read file operation

        try:
            with open(log_path, operation) as file:
                file = file.read().split("-")

                year, month, day = int(file[0]), int(file[1]), int(file[2])
                '''converting the date of the last backup it to delta object, 
                so we can substract it from the current date'''
                last_backup = date(year, month, day)

                days_diff = (current_date - last_backup).days  # getting the days difference

                # if the the difference was bigger than the re_backup value, the backp will start
                if days_diff >= re_backup:
                    # sending alert informing the start of the backup & last backup in days
                    Alerts(1, days_diff)
                    return 1

                else:
                    return sys.exit()

        except Exception as e:

            error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # the time of the error

            Error_log(e, error_time)  # calling the error log function to write to the error log
            Alerts(-1)  # there was an error, so alert will be sent
            sys.exit()  # exiting the program

    elif operation == 'w':  # if it was a file write operation

        try:

            with open(log_path, operation) as file:
                file.write(str(current_date))  # writting the new date to the log file

            Alerts(2, finish=finish)  # sending an alert regarding that the backup is done

            return 1

        except Exception as e:
            error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # the time of the error

            Error_log(e, error_time)  # calling the error log function to write to the error log
            Alerts(-1)  # there was an error, so alert will be sent
            sys.exit()  # exiting the program


def main():
    ''' Simple main function that is responsible for calling functions'''

    if os.path.exists(log_path):  # if the backup log already exists then read it
        Log_Backup('r')

    Backup(archive_path)
    Log_Backup('w')


#------------------------------------------------------------------------------------------------

##### VARIABLES YOU MUST NOT CHANGE #####

# this will get directory path of this file
current_folder: str = re.search(r'(.+\\).+$', __file__)[1]

current_date = date.today()  # Getting today's date
start: "time in seconds" = time.time()  # program execution start time
finish: "time in seconds" = None  # program execution end time

#------------------------------------------------------------------------------------------------

##### Variables you can change #####

# Optional [ default : the directory of this code file ] : is the list of paths you want to back up
file_sources: List[str] = [current_folder]

# Optional  [ default : is False ] : is the option of overwritting an existing archive that have the same name of the result archice
overwrite: bool = False

# Optional [ default : the directory of this code file ] : The destination of the backup process
archive_path: str = current_folder

# Optional [ default : the directory of this code file ] : the backup log file path,
log_path: str = f"{current_folder}backup.log"

# Optional [ default : the directory of this code file ] : the error log file path
error_path: str = f"{current_folder}error.log"

# Optional [ default : empty list [] ] : is a list of paths of files or folders that you don't want to include in the backup process
ignore_path: List[None] = []

# Optional [ default : 7 ] : is the certain number of days to backup again
re_backup: int = 7

#------------------------------------------------------------------------------------------------

# Program start

if __name__ == '__main__':
    main()
''' 

the backup log file format :

 YYYY-MM-DD

You mustn't edit the file contents or name to keep the program running normally

I'm not responsible for any data loss.

'''
