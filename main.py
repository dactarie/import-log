import paramiko  # pour le ssh remote
import shutil  # pour l'archive
import os  # pour la var home
import time  # pour le time wait
import datetime  # pour la date de fin de fichier
import threading  # Pour le multi thread

# Variables
path_server = os.environ["HOME"] + "/log/"  # ou vous souhaitez importé vos fichiers (STEP 4)
path_tmp = "/tmp/"  # dossier Temp sur le serveur et l'hote (STEP 4)
log_paramiko = '/tmp/paramiko.log'  # Log Paramiko (STEP 4)
login = 'root'  # Votre utilisateur pour SSH connect (STEP 4)
# Fin des variables


class Launch:
    def __init__(self, customer):
        self.host = customer
        self.date = datetime.datetime.now()
        self.remote_folder = path_tmp + customer
        self.remote_archive = path_tmp + customer + ".tar.gz"
        self.dst_archive = path_tmp + customer + ".tar.gz"
        self.dst_folder = path_server + customer + "/"
        self.archive = path_tmp + customer + ".tar.gz"
        self.ssh = paramiko.SSHClient()  # Seulement pour Paramiko
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Seulement pour Paramiko
        self.port = 22  # Seulement pour Paramiko
        self.paramiko_log = log_paramiko  # Seulement pour Paramiko
        paramiko.util.log_to_file(self.paramiko_log)  # Seulement pour Paramiko
        self.ssh.connect(hostname=self.host, port=self.port, username=login)  # Seulement pour Paramiko
        self.sftp = self.ssh.open_sftp()  # Seulement pour Paramiko

    def thread_function(self):  # lancement des fonctions (une version ultérieur prendra en charge le retour d'état).
        execution = Launch(self.host)
        execution.grouping()
        execution.create_tar()
        execution.import_files()
        execution.unpack()
        execution.remove_trace()
        execution.close_ok()
        execution.fast_scan()

    def grouping(self):  # Cette fonction regroupe les fichiers dans /path_tmp/name_of_your_customer.
        self.ssh.exec_command("mkdir " + self.remote_folder)  # crée le dossier /path_tmp/name_of_your_customer.
        with open("customer/" + self.host, "r") as list_of_files:  # pour chaque host
            dl = [line.strip() for line in list_of_files]  # Sort une ligne (un fichier)
            for g in range(len(dl)):  # pour chaque fichier dans l'host
                from os.path import basename
                name_of_file = basename(dl[g])
                self.ssh.exec_command("mkdir " + self.remote_folder + "/" + name_of_file)
                # cree un dossier du nom du fichiers
                self.ssh.exec_command("cp " + dl[g] + " " + self.remote_folder + "/" + name_of_file +
                                      "/" + name_of_file + "-" + (self.date.strftime("%F")))  # heure en 2020-04-04
                #  copie les fichiers dans leurs dossiers respectif

    def create_tar(self):  # Cette fonction crée une archive de tout le contenu dans /path_tmp/name_of_your_customer.
        self.ssh.exec_command("cd " + self.remote_folder + " && tar -czf " + self.archive + " .")
        time.sleep(1)

    def import_files(self):  # Cette fonction importe l'archive sur votre serveur.
        self.sftp.get(self.remote_archive, self.dst_archive)

    def unpack(self):  # Cette fonction décompacte l'archive sur votre serveur.
        shutil.unpack_archive(self.dst_archive, self.dst_folder)

    def remove_trace(self):  # Cette fonction supprime le dossier de regroupement et
        # vide le contenu des fichiers précédement importé.
        self.sftp.remove(self.remote_archive)
        self.ssh.exec_command("rm -Rf " + self.remote_folder)  # supprime le dossier crée dans /path_tmp/
        os.remove(self.dst_archive)
        with open("customer/" + self.host, "r") as list_of_file:  # supprime le contenue des fichiers sur l'hote
            full_path_of_file = [line.strip() for line in list_of_file]
            for g in range(len(full_path_of_file)):
                from os.path import basename
                name_of_file = basename(full_path_of_file[g])
                size = os.path.getsize(path_server + self.host + "/" + name_of_file + "/" + name_of_file + "-" + 
                                       (self.date.strftime("%F")))
                if size != 0:
                    self.ssh.exec_command("> " + full_path_of_file[g])  # suppression du contenu des fichiers.
                else:
                    print("\x1b[43m" + "File : " + name_of_file + " on " + self.host + " is empty !" + '\033[0m')
                    # affiche une alerte sur fichier vide

    def close_ok(self):  # Cette fonction ferme ssh et sftp.
        self.sftp.close()
        self.ssh.close()
        print("\x1b[42m" + "Task " + self.host + " OK"'\033[0m')

    def fast_scan(self):  # En développement (creéra une alerte sur certains mot clé).
        with open("customer/" + self.host, "r") as f:
            list_of_name_of_file = [line.strip() for line in f]
            for name_of_file in range(len(list_of_name_of_file)):
                from os.path import basename
                files_to_scan = \
                    self.dst_folder + basename(list_of_name_of_file[name_of_file]) + "/" \
                    + basename(list_of_name_of_file[name_of_file]) + "-" + self.date.strftime("%F")
                with open(files_to_scan, "r") as toto:
                    if "host" in toto:
                        print("hello est un test de branch")
                    else:
                        pass


if __name__ == "__main__":  # Lancement du script en Multi-thread
    threads = list()
    all_name_of_customer = os.listdir('customer/')  # liste des hotes (STEP 2)
    for name_of_customer in range(len(all_name_of_customer)):  # lance une instance pour chaque host
        a = Launch(all_name_of_customer[name_of_customer])
        x = threading.Thread(target=a.thread_function)
        threads.append(x)
        x.start()
