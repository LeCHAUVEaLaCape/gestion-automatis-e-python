import os
import shutil
from ftplib import FTP

# Navigation dans l'arborescence des répertoires
def navigate_directory(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))

# Changement de répertoire
def change_directory(path):
    os.chdir(path)

# Liste des fichiers et répertoires
def list_directory(path):
    return os.listdir(path)

# Renommage d'un fichier ou d'un répertoire
def rename(old_name, new_name):
    os.rename(old_name, new_name)

# Ajout d'un nouveau répertoire
def add_directory(path):
    os.mkdir(path)

# Copie d'un fichier ou d'un répertoire
def copy(source, destination):
    if os.path.isdir(source):
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)

# Déplacement d'un fichier ou d'un répertoire
def move(source, destination):
    shutil.move(source, destination)

# Suppression d'un fichier ou d'un répertoire
def delete(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

# Connexion au serveur FTP et sauvegarde des fichiers
def ftp_backup(host, username, password, source, destination):
    ftp = FTP(host)
    ftp.login(user=username, passwd=password)
    with open(source, 'rb') as file:
        ftp.storbinary('STOR ' + destination, file)

# Ajustez les valeurs pour correspondre à votre environnement
ftp_backup('ftp.example.com', 'username', 'password', 'C:/local/path', '/remote/path')

# etc...
