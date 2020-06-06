#! /usr/bin/pythonw
import re, paramiko, os
import ssh_executror.py


# ipadresses, ports, credentinals for the servers
host_1, port_1 = "192.168.64.121", 22
host_2, port_2 = "192.168.64.122", 22
host_3, port_3 = "192.168.64.123", 22
username, password = "root", "password"

# remote path ( where will be located transfering packages)
filepath = "/home/"
# local path ( where the packages right now)
localpath = "/Users/alex/Documents/test_files/"
#log file
paramiko.util.log_to_file("paramiko.log")

# select new rpm packeges from localpath
def sel_local_files(localpath):
    files_in_ldir = os.listdir(localpath)
    print(files_in_ldir)

# Regex of specific rpm packages
def find_files(file):
    Regex = re.compile(r'^servicepattern')
    Result = Regex.search(file)
    return Result



# connect to sftp
def connection(host, port):
    # Open a transport
    transport = paramiko.Transport((host, port))
    # Auth
    transport.connect(None, username, password)
    # Go!
    sftp = paramiko.SFTPClient.from_transport(transport)
    # show files in dir
    list_of_files = sftp.listdir(path=filepath)
    for file in list_of_files:
        if find_files(file) != None:
            sftp.remove(os.path.join(filepath, file))
            print(f'The next file: {file} has been removed \n')
    files_in_local_dir = os.listdir(localpath)
    for file in files_in_local_dir:
        if find_files(file) != None:
            sftp.put(os.path.join(localpath, file), os.path.join(filepath, file))
            print(f'The next file has been transfered: {file}')
    print(f"{host} - Success! \n")
    # Close
    if sftp: sftp.close()
    if transport: transport.close()

# connect to ssh and install packages
def ssh_conection(host, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('yum --nogpgcheck localinstall /home/servicepattern-*.rpm -y')
    #data = stdout.read() + stderr.read()
    data = stdout.read().decode('UTF-8')
    data_er = stderr.read().decode('UTF-8')
    if bool(data) != False:
        print(data)
    if bool(data_er) == True:
        print('ERROR: the next happened wrong: \n')
        print(data_er)
    else:
        print(f'{host}: SUCCESS: Installation has been completed!')
    client.close()

connection(host_1, port_1)
ssh_conection(host_1, port_1)
connection(host_2, port_2)
ssh_conection(host_2, port_2)
connection(host_1, port_1)
ssh_conection(host_3, port_3)




