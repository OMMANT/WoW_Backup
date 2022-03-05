import os
import zipfile
from tqdm import tqdm
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime

wow_path = Path('C:\Program Files (x86)\World of Warcraft\_retail_')
backup_path = wow_path / 'Backup'

if __name__ == '__main__':
    print('WoW Addon & Settings Backup Program v1.2 - by OMM')
    print('===============================================')
    now = datetime.now()
    file_name = now.strftime('%y%m%d_%H_%M_%S.zip')
    print(f'Backup File name: {file_name}')
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
    print('Done!')

