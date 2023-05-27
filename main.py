import os
import logging
import getpass
from ftplib import FTP, error_perm

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileManager:
    def __init__(self, ftp_host, username):
        self.ftp = FTP(ftp_host)
        password = getpass.getpass('Entrez votre mot de passe: ')
        try:
            self.ftp.login(username, password)
            logging.info("Connexion réussie au serveur FTP.")
        except error_perm as e:
            logging.error("Échec de la connexion FTP. Veuillez vérifier votre nom d'utilisateur et votre mot de passe.")
            raise e

    def navigate_directory(self, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                logging.info(f"Fichier trouvé : {os.path.join(root, name)}")
            for name in dirs:
                logging.info(f"Répertoire trouvé : {os.path.join(root, name)}")

    def upload_file(self, file, remote_directory):
        with open(file, 'rb') as f:
            try:
                self.ftp.storbinary('STOR %s' % os.path.join(remote_directory, os.path.basename(file)), f)
                logging.info(f"Fichier transféré avec succès : {file}")
            except error_perm as e:
                logging.error(f"Échec du transfert du fichier : {file}")
                raise e

    def create_remote_directory(self, directory):
        try:
            self.ftp.mkd(directory)
            logging.info(f"Répertoire créé avec succès : {directory}")
        except error_perm as e:
            logging.error(f"Échec de la création du répertoire : {directory}. Il se peut qu'il existe déjà, ou que vous n'ayez pas la permission de le créer.")
            raise e

    def upload_directory(self, local_directory, remote_directory):
        for root, dirs, files in os.walk(local_directory):
            for dir in dirs:
                self.create_remote_directory(os.path.join(remote_directory, dir))
            for file in files:
                self.upload_file(os.path.join(root, file), os.path.join(remote_directory, os.path.relpath(root, local_directory)))

# Test
username = input("Entrez votre nom d'utilisateur: ")
file_manager = FileManager('localhost', username)
file_manager.navigate_directory('/home/test/test_dir')
file_manager.upload_directory('/home/test/test_dir', '/srv/files/ftp')
