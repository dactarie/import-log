import paramiko
import shutil
import os
import time
import datetime
import threading

#  Variables
path_cible = os.environ["HOME"] + "/log/"  # Where your want to import your file(s) (STEP 4)
path_tmp_client = "/tmp/"  # Folder Temp On remote AND local (STEP 4)
log_paramiko = '/tmp/paramiko.log'  # Log Paramiko (STEP 4)
login = 'root'  # Your user for SSH connect (STEP 4)
# Fin des variables


class Lancement:
    def __init__(self, host):
        self.host = host
        self.date = datetime.datetime.now()
        self.src_folder = path_tmp_client + host
        self.remote_file = path_tmp_client + host + ".tar.gz"
        self.dst_file = path_tmp_client + host + ".tar.gz"
        self.dst_folder = path_cible + host + "/"
        self.archive = path_tmp_client + host + ".tar.gz"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.port = 22
        self.username = login
        self.paramiko_log = log_paramiko
        paramiko.util.log_to_file(self.paramiko_log)
        self.ssh.connect(hostname=self.host, port=self.port, username=self.username)
        self.sftp = self.ssh.open_sftp()

    def thread_function(self):
        execution = Lancement(self.host)
        execution.regroupement()
        execution.creation_archive()
        execution.import_fichiers()
        execution.decompactage()
        execution.supression()
        execution.close_ok()
        execution.scan_rapide()

    def regroupement(self):
        print(self.host + " regroupement")
        self.ssh.exec_command("mkdir " + self.src_folder)
        with open("srv/" + self.host, "r") as f:
            dl = [line.strip() for line in f]
            for g in range(len(dl)):
                from os.path import basename
                nom_de_fichier = basename(dl[g])
                self.ssh.exec_command("mkdir " + self.src_folder + "/" + nom_de_fichier)
                self.ssh.exec_command("cp " + dl[g] + " " + self.src_folder + "/" + nom_de_fichier +
                                      "/" + nom_de_fichier + "-" + (self.date.strftime("%F")))

    def creation_archive(self):
        print(self.host + " creation archive")
        self.ssh.exec_command("cd " + self.src_folder + " && tar -czf " + self.archive + " .")
        time.sleep(1)

    def import_fichiers(self):
        print(self.host + " Import archive")
        self.sftp.get(self.remote_file, self.dst_file)

    def decompactage(self):
        print(self.host + " Décompactage archive")
        shutil.unpack_archive(self.dst_file, self.dst_folder)

    def supression(self):
        print(self.host + " Suppression")
        self.sftp.remove(self.remote_file)
        self.ssh.exec_command("rm -Rf " + self.src_folder)
        os.remove(self.dst_file)
        with open("srv/" + self.host, "r") as f:
            full_path_of_file = [line.strip() for line in f]
            for g in range(len(full_path_of_file)):
                from os.path import basename
                nom_de_fichier = basename(full_path_of_file[g])
                taille = os.path.getsize(path_cible + self.host + "/" + nom_de_fichier + "/" + nom_de_fichier + "-" +
                                         (self.date.strftime("%F")))
                if taille != 0:
                    self.ssh.exec_command("> " + full_path_of_file[g])
                else:
                    print("le fichier " + nom_de_fichier + " sur " + self.host + " est vide !")
                    print(full_path_of_file)

    def close_ok(self):
        self.sftp.close()
        self.ssh.close()
        print('\x1b[6;30;46m' + "##### Ok pour " + self.host + " #####"'\033[0m')

    def scan_rapide(self):
        print("- Scan rapide des fichiers.")
        with open("srv/" + self.host, "r") as f:
            dl = [line.strip() for line in f]
            for g in range(len(dl)):
                from os.path import basename
                fichier_a_scanner = \
                    self.dst_folder + basename(dl[g]) + "/" + basename(dl[g]) + "-" + self.date.strftime("%F")
                with open(fichier_a_scanner, "r") as toto:
                    if "cible" in toto:
                        pass
                    else:
                        pass


if __name__ == "__main__":
    threads = list()
    all_name_of_host = os.listdir('srv/')  # Folder for list of server(s) (STEP 2)
    for i in range(len(all_name_of_host)):
        a = Lancement(all_name_of_host[i])
        x = threading.Thread(target=a.thread_function)
        threads.append(x)
        x.start()
