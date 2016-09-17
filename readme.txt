Readme:

In order to automate the backup process, you need to make a shortcut to 'runscript.vbs' and place it into the Startup folder (Start -> Search for: "shell:startup")

The script will be run everyday after 2 mins (120s) when you start windows.
To change this, edit the 'runscript.vbs' file

The actual backup of files is done only from 5 to 5 days (by default)
(To change this, edit the config file)

'runscript.vbs' will also show the terminal window when copying files
'runscript_background.vbs' does the work in background
(You have to choose only ONE of them)



Config file:

store_backups_folder - Where to deposit all the folders with backups
folders - list with folders that you want to make a backup to
	(use '/' for folder delimitators)
history_limit - how many backups to store for each folder
	(eg. if set to 3, there will always be no more than 3 backup folders for one of the folders you 	specify -> each time a new backup occurs, the oldest folder is removed)
backup_interval - how often (in  days) should the backup take place
last_backup - date when last update took place
