# Backup

#  Python tool that backup your files

### This tool can backup your files to anywhere you want, whether to your drive or your USB drive, it simply archive the files with the `tar` format **(= without compress)** to the path you specify.

### The tool is designed that it runs after a certain number of days with the help of two things :

#### 1- the `re_backup` variable ( default is 7 ) this variable is the certain number of days; the count starts since the written date in the `backup log` file which will be disussed after this line.

#### 2- the `backup log` file which will contain the last successful backup's date. 

### However, you need to find a way to let it run automatiaclly every day to check if it passed the `re_backup` number

## Editable variables -

#### `archive_path` ( Optional ) [ default : the directory of this code file ] : is the destination path of the resulted archive

#### `overwrite` ( Optional ) [ Default is False ] : is the option of overwritting an existing archive that have the same name of the result archice

#### `file_sources` ( Optional ) [ default : the directory of this code file ] : is a list of paths that you want to back up

#### `log_path` ( Optional )  [ default : the directory of this code file ] : is the path of the `backup log` file

#### `error_path` ( Optional )  [ default : the directory of this code file ] : is the path of the `error log` file

#### `re_backup` ( Optional ) [ Default is 7 days ] : Is the certain number of days to backup again

#### `ignore_path` ( Optional ) [ Default is empty list ] : is a list of paths of files or folders that you don't want to include in the backup process


## Steps -

#### 1- Download the code and the `backup log file` and pip install the modules in requirements.txt .

#### 2- Change the editable variables according to your desires

#### 3- run the program.


## Important notes -

#### to overwrite that existing archive with the result archice, you need to pass True to the `overwrite` variable.

> **The data that will be overwritten will be deleted permanently.**

#### The only thing left is to find your own way to let this program execute whenever you turn on your pc ( automating the script )

#### You mustn't edit the `backup log` file contents to prevent errors.

#### I'm not responsible for any data loss.

## additional info.

#### The date in `log file` must be in this format :

 `YYYY-MM-DD`

#### example :

 `2023-04-17`
