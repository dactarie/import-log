import paramiko
import shutil
import os
import time
import datetime
import threading

# Variables
path_server = os.environ["HOME"] + "/log/"  # Where your want to import your file(s) (STEP 4)
path_tmp = "/tmp/"  # Folder Temp On remote and local (STEP 4)
log_paramiko = '/tmp/paramiko.log'  # Log Paramiko (STEP 4)
login = 'root'  # Your user for SSH connect (STEP 4)
# End of variables


class Launch:
    def __init__(self, customer):
        self.host = customer
        self.date = datetime.datetime.now()
        self.remote_folder = path_tmp + customer
        self.remote_archive = path_tmp + customer + ".tar.gz"
        self.dst_archive = path_tmp + customer + ".tar.gz"
        self.dst_folder = path_server + customer + "/"
        self.archive = path_tmp + customer + ".tar.gz"
        self.ssh = paramiko.SSHClient()  # Only for Paramiko
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Only for Paramiko
        self.port = 22  # Only for Paramiko
        self.paramiko_log = log_paramiko  # Only for Paramiko
        paramiko.util.log_to_file(self.paramiko_log)  # Only for Paramiko
        self.ssh.connect(hostname=self.host, port=self.port, username=login)  # Only for Paramiko
        self.sftp = self.ssh.open_sftp()  # Only for Paramiko

    def thread_function(self):
        execution = Launch(self.host)
        execution.grouping()
        execution.create_tar()
        execution.import_files()
        execution.unpack()
        execution.remove_trace()
        execution.close_ok()
        execution.fast_scan()

    def grouping(self):  # This function grouping all your file into /path_tmp/name_of_your_customer.
        self.ssh.exec_command("mkdir " + self.remote_folder)
        with open("customer/" + self.host, "r") as list_of_files:
            dl = [line.strip() for line in list_of_files]
            for g in range(len(dl)):
                from os.path import basename
                name_of_file = basename(dl[g])
                self.ssh.exec_command("mkdir " + self.remote_folder + "/" + name_of_file)
                self.ssh.exec_command("cp " + dl[g] + " " + self.remote_folder + "/" + name_of_file +
                                      "/" + name_of_file + "-" + (self.date.strftime("%F")))

    def create_tar(self):  # This function create a archive of all content in /path_tmp/name_of_your_customer.
        self.ssh.exec_command("cd " + self.remote_folder + " && tar -czf " + self.archive + " .")
        time.sleep(1)

    def import_files(self):  # This function import archive on your server.
        self.sftp.get(self.remote_archive, self.dst_archive)

    def unpack(self):  # This function unpack archive on your server.
        shutil.unpack_archive(self.dst_archive, self.dst_folder)

    def remove_trace(self):  # This function remove all your trace and clean your files in your customer.
        self.sftp.remove(self.remote_archive)
        self.ssh.exec_command("rm -Rf " + self.remote_folder)
        os.remove(self.dst_archive)
        with open("customer/" + self.host, "r") as list_of_file:
            full_path_of_file = [line.strip() for line in list_of_file]
            for g in range(len(full_path_of_file)):
                from os.path import basename
                name_of_file = basename(full_path_of_file[g])
                size = os.path.getsize(path_server + self.host + "/" + name_of_file + "/" + name_of_file + "-" + 
                                       (self.date.strftime("%F")))
                if size != 0:
                    self.ssh.exec_command("> " + full_path_of_file[g])  # suppress content of file.
                else:
                    print("\x1b[43m" + "File : " + name_of_file + " on " + self.host + " is empty !" + '\033[0m')

    def close_ok(self):  # This function close ssh and sftp.
        self.sftp.close()
        self.ssh.close()
        print("\x1b[42m" + "Task " + self.host + " OK"'\033[0m')

    def fast_scan(self):
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


if __name__ == "__main__":  # Launch this script in Multi-thread.
    threads = list()
    all_name_of_customer = os.listdir('customer/')  # Folder for list of server(s) (STEP 2)
    for name_of_customer in range(len(all_name_of_customer)):
        a = Launch(all_name_of_customer[name_of_customer])
        x = threading.Thread(target=a.thread_function)
        threads.append(x)
        x.start()
