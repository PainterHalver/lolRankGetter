import base64
import yaml
import config

# GET AND PARSE THE 'LOCKFILE'
try:
    path = config.lockfilepath
    file = open(path)
except:
    input("'lockfile' not found! Maybe open the client first? Press Enter to exit...")

lockfile = file.readline().split(":")

port = lockfile[2]
username = 'riot'
password = lockfile[3]

# ENCODE TO base64 AUTH CODE
message = f"{username}:{password}"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
authCode = base64_bytes.decode('ascii')