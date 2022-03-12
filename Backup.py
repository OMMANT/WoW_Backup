import os
import fire
import zipfile
from tqdm import tqdm
from pathlib import Path
from time import strftime
from zipfile import ZipFile
from datetime import datetime

wow_path = Path('C:\Program Files (x86)\World of Warcraft\_retail_')
backup_path = wow_path / 'Backup'
now = datetime.now()

def backup(force=False, check=True, file_name=now.strftime('%y%m%d_%H_%M_%S.zip')):
    if force or (check and check_compressing()):
        for_zip = ['Fonts', 'Interface', 'WTF']
        print(f'Backup {for_zip} to {str(backup_path / file_name)}')
        print('Compressing.', end='')
        sec = datetime.now().second
        with ZipFile(backup_path / file_name, 'w') as zip_file:
            for fz in for_zip:
                for folder, _, files in os.walk(wow_path / fz):
                    folder = Path(folder)
                    for file in files:
                        s = datetime.now().second
                        if s != sec:
                            print('.', end='')
                            sec = s
                        zip_file.write(folder / file, os.path.relpath(folder / file, wow_path), compress_type=zipfile.ZIP_DEFLATED)
        print('\nCompressed!!')
        print('Check for removing backup file')
        zip_files = [x for x in os.listdir(backup_path) if x.endswith('.zip')]
        n = len(zip_files) - 30
        if n > 0:
            for rm in tqdm(zip_files[:n]):
                p = backup_path / rm
                os.remove(p)


def check_compressing():
    try:
        recent_file = [x for x in os.listdir(backup_path) if x.endswith('.zip')][-1].split('_')
        ## Pass compressing (same day within 3 hours)
        same_day = now.strftime('%y%m%d') == recent_file[0]
        within3hours = int(now.strftime('%H')) <= int(recent_file[1])
        if same_day and within3hours:
            print('Compressed recently!')
        else: return True
    except IndexError:
        return True    


if __name__ == '__main__':
    print('WoW Addon & Settings Backup Program v1.2 - by OMM')
    print('===============================================')
    fire.Fire(backup)
    print('Done!')

