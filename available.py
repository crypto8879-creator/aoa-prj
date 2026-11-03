import shutil

original_file = 'data.txt'
backup_file = 'backup_data.txt'

shutil.copyfile(original_file, backup_file)
print("Backup completed!")