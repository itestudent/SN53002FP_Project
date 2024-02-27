from utils.config_loader import load_config
from utils.logger import get_logger, handle_error
from utils.ftp_client import FTPClient
from utils.file_service import FileService

class StorageManager:
    USER_NAME = 'itestudent'
    CONFIG_PATH = 'config.txt'

    def __init__(self):
        self.logger = get_logger(StorageManager.USER_NAME)
        try:    
            self.config = load_config(StorageManager.CONFIG_PATH)
            self.ftp = FTPClient(self.config.server.ip_address)
            self.file_service = FileService
        except Exception as e:
            self.logger.error('Failed initialising script : ' + str(e))

    # 1. Download folder from remote
    @handle_error('Failed downloading file from ftp')
    def download_files(self):
        self.ftp.download_directory(self.config.server.folder, self.config.client.folder)
        self.logger.info('Downloading file from ftp done.')

    # 2. Separate files by type
    @handle_error('Failed file sorting')
    def separate_files(self):
        self.file_service.separate_files(
            origin_directory = self.config.client.folder,
            images_directory = self.config.client.image_folder,
            text_directory = self.config.client.text_folder
        )
        self.logger.info('File sorting done.')

    # 3. Scan and quarantine viruses
    @handle_error('Failed virus scan')
    def scan_viruses(self):
        self.file_service.scan_and_quarantine_viruses(
            origin_directory = self.config.client.text_folder,
            quarantine_directory = self.config.client.virus_folder
        )
        self.logger.info('Scan file for virus done.')

    # 4. Zip files by month and file type
    @handle_error('Failed file archiving')
    def archive_files_by_month(self):
        self.file_service.zip_files_by_month(
            source_directory = self.config.client.image_folder,
            zip_destination_directory = self.config.client.zip_folder,
            zip_suffix = 'img',
            password = StorageManager.USER_NAME
        )
        self.file_service.zip_files_by_month(
            source_directory = self.config.client.text_folder,
            zip_destination_directory = self.config.client.zip_folder,
            zip_suffix = 'txt',
            password = StorageManager.USER_NAME
        )
        self.logger.info('Archive file done.')

    # 5. Ping and upload zip files to server
    @handle_error('Failed to upload zip file')
    def upload_archive_files(self):
        self.ftp.wait_for_connection(
            max_retry_count = 2,
            retry_seconds_interval = 5
        )
        self.logger.info('Ping ftp connectivity done.')
        self.ftp.upload_files(
            from_local_directory = self.config.client.zip_folder,
            to_remote_directory = self.config.server.zip_folder
        )
        self.logger.info('Upload zip file done.')

    # automation script pipeline runner
    def run_script_pipeline(self):
        self.download_files()
        self.separate_files()
        self.scan_viruses()
        self.archive_files_by_month()
        self.upload_archive_files()

if __name__ == '__main__':
    manager = StorageManager()
    manager.run_script_pipeline()