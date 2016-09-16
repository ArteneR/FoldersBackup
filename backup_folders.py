import re
import json
import datetime
from datetime import date
from distutils.dir_util import copy_tree
from os import listdir
from os.path import isfile, join


config_filename = "config.json"
config = None
store_backups_folder = None
folders = None
history_limit = None



def compareDates(date1, date2):
    delta = date1 - date2
    return delta.days



def stringToDate(date_string):
    chunks = date_string.split('-')
    return date(int(chunks[0]), int(chunks[1]), int(chunks[2]))



def update_last_backup_date(new_last_backup_date):
    global config
    config["last_backup"] = str(new_last_backup_date)



def update_config_file():
    global config
    global config_filename
    with open(config_filename, 'w') as config_file_out:
        json.dump(config, config_file_out)
        config_file_out.close()



def read_config_file():
    global config
    global folders
    global store_backups_folder
    global history_limit
    with open(config_filename) as  config_file:
        config = json.load(config_file)

        store_backups_folder = config["store_backups_folder"]
        store_backups_folder = store_backups_folder.rstrip('/')
        backup_interval = config["backup_interval"]
        last_backup = config["last_backup"]
        folders = config["folders"]
        history_limit = config["history_limit"]

        today_formatted = datetime.date.today()
        last_backup_formatted = stringToDate(last_backup)
        days_difference = compareDates(today_formatted, last_backup_formatted)

        # if today - last_backup >= backup_interval
        if (days_difference >= backup_interval or days_difference < 0):
            print('Its backup time!!!')
            backup_all_folders()
            update_last_backup_date(today_formatted)
            update_config_file()
        else:
            print('No backup is going to happen today :(. Next backup should take place after %s day/s' % (backup_interval - days_difference))
        config_file.close()



def backup_all_folders():
    for folder in folders:
        backup_folder(folder)



def backup_folder(folder_path):
    today_formatted = datetime.date.today()

    fromDirectory = folder_path.rstrip('/')

    toDirectoryName = fromDirectory.replace(":", "")
    toDirectoryName = toDirectoryName.replace("/", "-")
    toDirectoryName += "_" + str(today_formatted)
    toDirectory = store_backups_folder + "/" + toDirectoryName
    checkOldFolders(toDirectory)

    print('Copying files from %s folder to %s folder...' % (fromDirectory, toDirectory))
    copy_tree(fromDirectory, toDirectory)
    print('Copied successfully!')



def checkOldFolders(folder_path):
    folder_path_components = folder_path.rsplit('/', 1)
    folder_parent = folder_path_components[0]
    folder_name = folder_path_components[1]
    folder_name_clean = folder_name.rsplit('_', 1)[0]

    old_folders = []

    for folder in listdir(store_backups_folder):
        pattern = re.compile(folder_name_clean+'_.{4}-.{2}-.{2}')
        matchObj = pattern.match(folder)

        if matchObj:
           old_folders.append(matchObj.group())

    print('Old folders list:')
    print(old_folders)

    print('Folder parent: %s' % folder_parent)
    print('Folder name clean: %s' % folder_name_clean)


if __name__ == "__main__":
    read_config_file()
    print('\nOperation finished successfully!\n')