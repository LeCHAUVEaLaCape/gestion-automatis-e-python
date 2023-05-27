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
            logging.info(f"Répertoire {directory} existant déjà, aucune action nécessaire.")

    def upload_directory(self, local_directory, remote_directory):
        for root, dirs, files in os.walk(local_directory):
            for dir in dirs:
                remote_dir = os.path.join(remote_directory, os.path.relpath(root, local_directory), dir)
                self.create_remote_directory(remote_dir)
            for file in files:
                remote_dir = os.path.join(remote_directory, os.path.relpath(root, local_directory))
                self.upload_file(os.path.join(root, file), remote_dir)

username = input("Entrez votre nom d'utilisateur: ")
file_manager = FileManager('localhost', username)
file_manager.upload_directory('/home/test/test_dir', '/srv/files/ftp')
