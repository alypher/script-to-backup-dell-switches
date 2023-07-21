import datetime
import paramiko
from time import sleep

# Variables to script
st = datetime.datetime.now().strftime("%d-%B-%Y")

class Host(): 
    def __init__(self, ip, username, password, enable_password, name):
        self.ip = ip
        self.username = username 
        self.password = password 
        self.enable_password = enable_password 
        self.name = name

# Variables for hosts
hosts = [
    Host('10.8.0.101', 'admin', 'pass1', 'pass1!', 'sw-1'),
    Host('10.8.0.110', 'admin', 'pass2', 'pass2!', 'sw-2'),
    Host('10.8.0.99', 'admin', 'pass3', 'pass3!', 'sw-3'),
]

tftp_server = '10.8.0.19'

def do_backup_to_tftp(host):
    # Start client connection
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(getattr(host, 'ip'), username=getattr(host, 'username'), password=getattr(host, 'password'), port=22)
    print("connected to {} as {}".format(getattr(host, 'name'), getattr(host, 'username')))
    sleep(5)
    
    # Start shell to send commands
    remote_conn = client.invoke_shell()
    sleep(2)
    remote_conn.send('enable'+"\n")
    sleep(2)
    remote_conn.send(getattr(host, 'enable_password')+'\n')
    sleep(2)
    # remove this line below on production:
    # remote_conn.send(("show startup-config"+"\n"))
    
    # use this commands below to copy backup to a TFTP server
    remote_conn.send("copy running-config tftp://"+tftp_server+"/"+getattr(host, 'name')+"-"+st+".txt\n")
    sleep(2)
    remote_conn.send(("y"+"\n"))
    sleep(2)

    # Print output
    output = remote_conn.recv(10000)
    print(output)

    # Close connection
    client.close()

for host in hosts:
    print('\nStarting backup on host:'+getattr(host, 'name')+"\n")
    do_backup_to_tftp(host)
