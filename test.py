import paramiko
import os
import datetime

date = datetime.datetime.now()
print(date)
paramiko.util.log_to_file('/tmp/paramiko.log')
directory = "logs"
emplacement = "/tmp/logs/"
remote_file = ["/var/log/syslog", "/var/log/auth.log"]
host = 'cible2'
port = 22
username = 'root'

path = os.path.join(emplacement, host)
file_to_copy = path + "/" + "syslog " + (date.strftime("%Y-%m-%d %H:%M:%S"))

# Creation de dossier
try:
    os.mkdir(emplacement)
except OSError as error:
    print(error)

try:
    os.mkdir(path)
except OSError as error:
    print(error)

# import des fichiers
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect(hostname=host, port=port, username=username)

sftp = ssh.open_sftp()
for x in file_to_copy:
    sftp.get(remote_file, file_to_copy)

    print(file_to_copy)

sftp.close()
ssh.close()
