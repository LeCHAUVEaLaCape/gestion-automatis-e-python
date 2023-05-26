import os
from ftplib import FTP

class FileManager:
    def __init__(self, ftp_host, ftp_user, ftp_password):
        self.ftp = FTP(ftp_host)
        self.ftp.login(ftp_user, ftp_password)

    def navigate_directory(self, path):
        # Naviguer dans un répertoire
        for root, dirs, files in os.walk(path):
            for name in files:
                print(os.path.join(root, name))
            for name in dirs:
                print(os.path.join(root, name))

    def change_directory(self, path):
        # Changer de répertoire
        os.chdir(path)

    def upload_file(self, file, remote_directory):
        # Upload a file to the FTP server
        with open(file, 'rb') as f:
            self.ftp.storbinary('STOR %s' % os.path.join(remote_directory, os.path.basename(file)), f)

# Test
file_manager = FileManager('ftp.yourserver.com', 'username', 'password')
file_manager.navigate_directory('/home/user/test')
file_manager.change_directory('/home/user/test/new_directory')
file_manager.upload_file('/home/user/test/file.txt', '/remote/directory')
