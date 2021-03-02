#!/usr/bin/python3
import socket
import os
import paramiko

nameofhost = (socket.gethostname())

directory = "/tmp/import"
try:
    os.mkdir(directory)
except OSError as error:
    print(error)


shutil.copy2('/var/log/syslog', '/tmp/import/syslog')
shutil.copy2('/var/log/auth.log', '/tmp/import/auth.log')

try:
    shutil.rmtree(directory)
except OSError as error:
    print(error)
