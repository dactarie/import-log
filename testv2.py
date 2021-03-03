import paramiko
import shutil
import os
import time

host = os.listdir('srv/')

#  Conf Paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
port = 22
username = 'root'
paramiko.util.log_to_file('/tmp/paramiko.log')
#  Fin de conf Paramiko


def regroupement():
    print("- Regroupement des fichiers dans " + remote_file)
    ssh.exec_command("mkdir " + src_folder)
    with open("srv/" + host[i], "r") as f:
        fichier = [line.strip() for line in f]
        for g in range(len(fichier)):
            ssh.exec_command("cp " + fichier[g] + " " + src_folder)


def creation_archive():
    print("- Creation de l'archive : " + remote_file)
    ssh.exec_command("cd " + src_folder + " && tar -czvf " + archive + " .")
    time.sleep(3)


def import_fichiers():
    print("- Import du fichier archive ici : " + remote_file + " a " + dst_file)
    sftp.get(remote_file, dst_file)


def decompactage():
    print("- Décompactage de larchive dans " + dst_folder)
    shutil.unpack_archive(dst_file, dst_folder)


def supression():
    print("- Suppression de l'archive distante + local " + remote_file + " " + dst_file)
    sftp.remove(remote_file)
    ssh.exec_command("rm -Rf " + src_folder)
    os.remove(dst_file)


def close_ok():
    sftp.close()
    ssh.close()
    print("##### Fin de la tache pour l'hote " + host[i] + " OK #####")


for i in range(len(host)):
    src_folder = "/tmp/" + host[i]
    remote_file = "/tmp/" + host[i] + ".tar.gz"
    dst_file = "/tmp/" + host[i] + ".tar.gz"
    dst_folder = "/home/guillaume/log/" + host[i] + "/"
    archive = "/tmp/" + host[i] + ".tar.gz"
    ssh.connect(hostname=host[i], port=port, username=username)
    sftp = ssh.open_sftp()
    regroupement()
    creation_archive()
    import_fichiers()
    decompactage()
    supression()
    close_ok()
