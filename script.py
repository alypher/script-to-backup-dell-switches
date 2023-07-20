import datetime
import paramiko
from time import sleep

# Variables to script
st = datetime.datetime.now().strftime("%d-%B-%Y")

# Variables for hosts
hosts = [
    '10.8.0.101',
    '10.8.0.110',
    '10.8.0.99'
]
username = 'admin'
password = 'password'
tftp_server = '10.8.0.19'

def do_backup_to_tftp(host, user, passwd):
    # Start client connection
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=passwd, port=22)
    print("connected to {} as {}".format(host, user))
    sleep(2)
    
    # Start shell to send commands
    remote_conn = client.invoke_shell()
    sleep(2)
    remote_conn.send('enable'+"\n")
    sleep(2)
    remote_conn.send(passwd+'\n')
    sleep(2)
    
    # use this commands below to copy backup to a TFTP server
    remote_conn.send("copy running-config tftp://"+tftp_server+"/"+host+"-"+st+".txt\n")
    sleep(2)
    remote_conn.send(("y"+"\n"))
    sleep(2)

    # Print output
    output = remote_conn.recv(1000)
    print(output)

    # Close connection
    client.close()

for host in hosts:
    print('\nStarting backup on host:'+host+"\n")
    do_backup_to_tftp(host, username, password)
