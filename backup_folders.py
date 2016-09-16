import re
import json
import datetime
import shutil
import os
import stat
from datetime import date
from distutils.dir_util import copy_tree
from os import listdir


config_filename = "config.json"
config_file = None
log_filename = "log.txt"
log_file = None
config = None
store_backups_folder = None
folders = None
history_limit = None
old_folders = []
folder_to_remove = None



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
    global config_file
    global folders
    global store_backups_folder
    global history_limit
    global log_filename
    global log_file

    log_file = open(log_filename, "a")
    log_file.write('\r\n')

    with open(config_filename) as  config_file:
        config = json.load(config_file)

        store_backups_folder = config["store_backups_folder"]
        store_backups_folder = store_backups_folder.rstrip('/')
        backup_interval = config["backup_interval"]
        last_backup = config["last_backup"]
        folders = config["folders"]
        history_limit = config["history_limit"]

        today_formatted = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M")
        last_backup_formatted = stringToDate(last_backup)
        days_difference = compareDates(today_formatted, last_backup_formatted)
        log_file.write('[' + str(today_formatted) + ' ' + str(current_time) + ']')

        # if today - last_backup >= backup_interval
        if (days_difference >= backup_interval or days_difference < 0):
            output_message('\nIts backup time!!!')
            backup_all_folders()
            update_last_backup_date(today_formatted)
            update_config_file()
        else:
            output_message('\nNo backup is going to happen today :(. Next backup should take place after %s day/s' % (backup_interval - days_difference))
        config_file.close()



def backup_all_folders():
    for folder in folders:
        backup_folder(folder)



def output_message(message):
    print(message)
    log_file.write(message)



def backup_folder(folder_path):
    today_formatted = datetime.date.today()
    permission_mode = stat.S_IRWXU

    fromDirectory = folder_path.rstrip('/')

    toDirectoryName = fromDirectory.replace(":", "")
    toDirectoryName = toDirectoryName.replace("/", "-")
    toDirectoryName += "_" + str(today_formatted)
    toDirectory = store_backups_folder + "/" + toDirectoryName

    output_message("\nCopying files from '%s' folder to '%s' folder..." % (fromDirectory, toDirectory))

    change_permissions_recursive(toDirectory, permission_mode)
    copy_tree(fromDirectory, toDirectory)

    output_message('\nCopied successfully!')

    checkOldFolders(toDirectory)



def checkOldFolders(folder_path):
    global old_folders
    old_folders_for_this_folder = []
    folder_path_components = folder_path.rsplit('/', 1)
    folder_name = folder_path_components[1]
    folder_name_clean = folder_name.rsplit('_', 1)[0]

    for folder in listdir(store_backups_folder):
        pattern = re.compile(folder_name_clean+'_.{4}-.{2}-.{2}')
        matchObj = pattern.match(folder)

        if matchObj:
           old_folders_for_this_folder.append(matchObj.group())

    old_folders.append(old_folders_for_this_folder)
    if len(old_folders_for_this_folder) >= history_limit:
        removeOldFolders()



def removeOldFolders():
    global folder_to_remove
    permission_mode = stat.S_IRWXU
    for old_folders_list in old_folders:
        if (len(old_folders_list) >= history_limit):
            old_folders_list.sort()
            for i in range(0, len(old_folders_list)-history_limit):
                folder_to_remove = store_backups_folder + "/" + old_folders_list[i]
                change_permissions_recursive(folder_to_remove, permission_mode)
                shutil.rmtree(folder_to_remove, onerror = on_rm_error)
                output_message("\n! Folder '%s' has been removed !" % folder_to_remove)
                old_folders_list.remove(old_folders_list[i])


def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dirs]:
            os.chmod(dir, mode)
        for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)


def on_rm_error():
    os.chmod(folder_to_remove, stat.S_IWRITE)
    os.unlink(folder_to_remove)


if __name__ == "__main__":
    read_config_file()
    output_message('\nOperation finished successfully!\n')
    log_file.write('\r\n')
    log_file.close()