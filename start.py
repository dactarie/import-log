import paramiko
import shutil
import os
import time
import datetime

#  variables
host = os.listdir('srv/')
path_cible = "/home/guillaume/log/"
path_tmp_client = "/tmp/"
#  Fin de variable

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
        dl = [line.strip() for line in f]
        for g in range(len(dl)):
            from os.path import basename
            nom_de_fichier = basename(dl[g])
            ssh.exec_command("mkdir " + src_folder + "/" + nom_de_fichier)
            ssh.exec_command("cp " + dl[g] + " " + src_folder + "/" + nom_de_fichier + "/" + nom_de_fichier + "-" +
                             (date.strftime("%F")))
            print(dl)
            taille = os.path.getsize(dl[g])
            if taille > 0:
                ssh.exec_command("> " + dl[g])
            else:
                print(dl[g])


def creation_archive():
    print("- Création de l'archive : " + remote_file)
    a,b,c = ssh.exec_command("cd " + src_folder + " && tar -czvf " + archive + " . && echo $?")
    print(b.channel.recv_exit_status())
    time.sleep(3)


def import_fichiers():
    print("- Import du fichier archive dans : " + remote_file + " a " + dst_file)
    sftp.get(remote_file, dst_file)


def decompactage():
    print("- Décompactage de l'archive dans " + dst_folder)
    shutil.unpack_archive(dst_file, dst_folder)


def supression():
    print("- Suppression de l'archive distante et local " + remote_file + " " + dst_file)
    sftp.remove(remote_file)
    ssh.exec_command("rm -Rf " + src_folder)
    os.remove(dst_file)


def close_ok():
    sftp.close()
    ssh.close()
    print("##### Fin de la tache pour l'hôte " + host[i] + " #####")


def analyse_rapide():
    print("- Scan rapide des fichiers.")
    with open("srv/" + host[i], "r") as f:
        dl = [line.strip() for line in f]
        for g in range(len(dl)):
            from os.path import basename
            fichier_a_scanner = dst_folder + basename(dl[g]) + "/" + basename(dl[g]) + "-" + date.strftime("%F")
            with open(fichier_a_scanner, "r") as toto:
                if "cible" in toto:
                    print("-")
                else:
                    print("-")


for i in range(len(host)):
    #  Variables
    date = datetime.datetime.now()
    src_folder = path_tmp_client + host[i]
    remote_file = path_tmp_client + host[i] + ".tar.gz"
    dst_file = path_tmp_client + host[i] + ".tar.gz"
    dst_folder = path_cible + host[i] + "/"
    archive = path_tmp_client + host[i] + ".tar.gz"
    ssh.connect(hostname=host[i], port=port, username=username)
    sftp = ssh.open_sftp()
    #  Fin des variables

    regroupement()
    creation_archive()
    import_fichiers()
    decompactage()
    supression()
    close_ok()
    analyse_rapide()
