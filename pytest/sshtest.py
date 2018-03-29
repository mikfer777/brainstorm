import os
import paramiko

paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.load_host_keys(os.path.expanduser('c:/rootCygwin/home/s227783/.ssh/known_hosts'))
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('172.24.136.36', 42124, username='webadm')
stdin, stdout, stderr = ssh.exec_command("ls /var/projects/AMM/weblogic_10.0MP1/DOMAINE-ALSB-AMM/log")
stdin.flush()
ftp = ssh.open_sftp()
data = stdout.read().splitlines()
for line in data:
        if line.endswith('yyyyMMdd'):
            print line
            
        

#ftp.get('socksumm.pl', 'socksumm.pl')
ftp.close()

ssh.close()