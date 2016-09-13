import json
import datetime
from datetime import date


config_filename = "config.json"
config = None
store_backups_folder = None
folders = None



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



def read_config_file():
    global config
    global folders
    global store_backups_folder
    with open(config_filename) as  config_file:
        config = json.load(config_file)

        store_backups_folder = config["store_backups_folder"]
        backup_interval = config["backup_interval"]
        last_backup = config["last_backup"]
        folders = config["folders"]

        today_formatted = datetime.date.today()
        last_backup_formatted = stringToDate(last_backup)
        days_difference = compareDates(today_formatted, last_backup_formatted)

        # if today - last_backup >= backup_interval
        if (days_difference >= backup_interval or days_difference < 0):
            print('Its backup time!!!')
            #backup_all_folders()
            update_last_backup_date(today_formatted)
            update_config_file()
        else:
            print('No backup is going to happen today :(. Next backup should take place after %s day/s' % (backup_interval - days_difference))


def backup_all_folders():
    for folder in folders:
        backup_folder(folder)



def backup_folder(folder):
    print('')



if __name__ == "__main__":
    read_config_file()