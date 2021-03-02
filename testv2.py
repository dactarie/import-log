import paramiko
import shutil
import datetime
import os
import time

date = datetime.datetime.now()
paramiko.util.log_to_file('/tmp/paramiko.log')
host = 'cible1'
log_to_export = "syslog,auth.log"

src_folder = "/tmp/" + host
remote_file = "/tmp/" + host + ".tar.gz"
dst_file = "/tmp/" + host + ".tar.gz"
dst_folder = "/home/guillaume/log/" + host + "/" + (date.strftime("%Y-%m-%d %H:%M:%S")) + "/"
archive = "/tmp/" + host + ".tar.gz"
port = 22
username = 'root'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
      paramiko.AutoAddPolicy())
ssh.connect(hostname=host, port=port, username=username)
sftp = ssh.open_sftp()

print("## regoupement des fichiers dans " + remote_file)
ssh.exec_command("mkdir " + src_folder)
ssh.exec_command("cp /var/log/{" + log_to_export + "} " + src_folder)
ssh.exec_command("cp /dev/null /var/log/{" + log_to_export + "} ")

print("## creation de l'archive " + remote_file)
ssh.exec_command("cd " + src_folder + " && tar -czvf " + archive + " .")
print(archive)
time.sleep(5)

print("## import du fichier archive ici " + remote_file + " a " + dst_file)
sftp.get(remote_file, dst_file)

print("## decompactage de larchive dans " + dst_folder)
shutil.unpack_archive(dst_file, dst_folder)

print("## supression de l'archive distante + local " + remote_file + " " + dst_file)
sftp.remove(remote_file)
ssh.exec_command("rm -Rf " + src_folder)
os.remove(dst_file)

sftp.close()
ssh.close()
print("## Fin de la tache ##")
