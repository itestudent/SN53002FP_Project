import os
import re
import shutil
from mimetypes import guess_type
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

from .encryption_service import EncryptionService

class FileService:
    #region utility file/directory methods
    @staticmethod
    def ensure_path_exists(directory_path: str):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    @staticmethod
    def get_files(directory_path: str):
        return os.listdir(directory_path)
    
    @staticmethod
    def move_file(from_path: str, to_path: str):
        shutil.move(from_path, to_path)
    #endregion

    #region separation by type methods
    @staticmethod
    def is_image_file(file_name: str):
        return 'image/' in guess_type(file_name)[0]
    
    @staticmethod
    def is_text_file(file_name: str):
        return 'text/' in guess_type(file_name)[0]

    @classmethod
    def separate_files(cls, origin_directory: str, images_directory: str, text_directory: str):
        # ensure paths exists first
        cls.ensure_path_exists(images_directory)
        cls.ensure_path_exists(text_directory)
        
        # loop through files
        files = cls.get_files(origin_directory)
        for file in files:
            from_path = os.path.join(origin_directory, file)

            # figure out which directory to move the file to
            to_directory = None
            if cls.is_image_file(file):
                to_directory = images_directory
            elif cls.is_text_file(file):
                to_directory = text_directory

            # move to destination directory if found
            if to_directory != None:
                to_path = os.path.join(to_directory, file)
                cls.move_file(from_path, to_path)
    #endregion
                
    #region virus identifier methods and members
    VIRUS_PATTERN = re.compile('[a-zA-Z]{2}[0-9]{6}')

    @classmethod
    def contains_virus_trace(cls, file_path: str):
        # read all lines
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # test for virus pattern in line
            for line in lines:
                matched_virus = cls.VIRUS_PATTERN.search(line)
                if matched_virus:
                    return True
        return False
    
    @classmethod
    def scan_and_quarantine_viruses(cls, origin_directory: str, quarantine_directory: str):
        viruses = []
        cls.ensure_path_exists(quarantine_directory)

        # loop through files
        files = cls.get_files(origin_directory)
        for file in files:
            file_path = os.path.join(origin_directory, file)

            # if contains virus trace, quarantine it
            if cls.contains_virus_trace(file_path):
                viruses.append(file)
                quarantine_path = os.path.join(quarantine_directory, file)
                cls.move_file(file_path, quarantine_path)

        return viruses
    #endregion
    
    #region file archiving and grouping methods
    @classmethod
    def group_files_by_month(cls, directory: str):
        file_paths_by_month: dict[str, set[str]] = {}

        # loop through files
        files = cls.get_files(directory)
        for file in files:
            file_path = os.path.join(directory, file)

            # parse created month
            created_time = os.path.getmtime(file_path)
            created_datetime = datetime.fromtimestamp(created_time)
            created_month = created_datetime.strftime('%Y%m')
            
            # collate groups by month
            if not created_month in file_paths_by_month:
                file_paths_by_month[created_month] = set()
            file_paths_by_month[created_month].add(file_path)

        return file_paths_by_month
    
    @classmethod
    def zip_files_by_month(cls, source_directory: str, zip_destination_directory: str, zip_suffix: str, password: str):
        cls.ensure_path_exists(zip_destination_directory)

        # group files by month
        file_paths_by_month = cls.group_files_by_month(source_directory)
        for month, file_paths in file_paths_by_month.items():

            # generate zip file name for each month's archive
            zip_file_name = month + '-' + zip_suffix + '.zip'
            zip_file_path = os.path.join(zip_destination_directory, zip_file_name)

            # create zip file with all file entries under that month
            zip_file = ZipFile(zip_file_path, 'w', ZIP_DEFLATED)
            for file_path in file_paths:
                zip_file.write(file_path, os.path.basename(file_path))
            zip_file.close()

            EncryptionService.encrypt_file(zip_file_path, password)
    #endregion
