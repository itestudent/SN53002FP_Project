import os
import time
from ftplib import FTP
from datetime import datetime

from .file_service import FileService

class FTPClient:
    def __init__(self, server_address: str):
        self._ftp = FTP()
        self._ftp.connect(server_address)
        self._ftp.login('anonymous', 'ite sucks')

    def __del__(self):
        self._ftp.quit()

    def _test_connection(self):
        try:
            self._ftp.voidcmd('NOOP')
            return True
        except:
            return False
        
    def wait_for_connection(self, max_retry_count: int, retry_seconds_interval: int):
        retry_count = 0
        connection_established = self._test_connection()
        while not connection_established and retry_count < max_retry_count:
            time.sleep(retry_seconds_interval)
            connection_established = self._test_connection()
            retry_count += 1
        if not connection_established:
            raise Exception('failed to connect to FTP server after ' + str(retry_count) + ' retries')

    def list_remote(self, directory: str) -> list[str]:
        return self._ftp.nlst(directory)

    def upload_file(self, from_local_path: str, to_remote_path: str):
        with open(from_local_path, 'rb') as bytes:
            self._ftp.storbinary('STOR ' + to_remote_path, bytes)

    def download_file(self, from_remote_path: str, to_local_path: str):
        with open(to_local_path, 'wb') as local_file:
            self._ftp.retrbinary('RETR ' + from_remote_path, local_file.write)

    def get_remote_modified_timestamp(self, remote_file_path: str):
        timestamp = self._ftp.voidcmd("MDTM " + remote_file_path)[4:].strip() #YYYYMMDD...
        parsed_datetime = datetime.now().replace(
            year = int(timestamp[0:4]),
            month = int(timestamp[4:6]),
            day = int(timestamp[6:8])
        )
        return parsed_datetime.timestamp()

    def download_directory(self, from_remote_directory: str, to_local_directory: str):
        FileService.ensure_path_exists(to_local_directory)

        # read remote and download each file
        remote_files = self.list_remote(from_remote_directory)
        for remote_file in remote_files:
            from_remote_path = os.path.join(from_remote_directory, remote_file)
            to_local_path = os.path.join(to_local_directory, remote_file)
            self.download_file(from_remote_path, to_local_path)

            # fetch modified timestamp, and persist it
            modified_timestamp = self.get_remote_modified_timestamp(from_remote_path)
            os.utime(to_local_path, (modified_timestamp, modified_timestamp))

    def upload_files(self, from_local_directory: str, to_remote_directory: str):
        # get files from local directory
        files = FileService.get_files(from_local_directory)

        # ensure remote directory exists
        if to_remote_directory not in self.list_remote('.'):
            self._ftp.mkd(to_remote_directory)

        # upload each file found to specified destination
        for file in files:
            from_local_path = os.path.join(from_local_directory, file)
            to_remote_path = os.path.join(to_remote_directory, file)
            self.upload_file(from_local_path, to_remote_path)
