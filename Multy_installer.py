#! /usr/bin/pythonw
import re, paramiko, os, configparser, tqdm, time, sys, tkinter, colorama
from tkinter import messagebox
from colorama import Fore, Back, Style
colorama.init()

# log file
paramiko.util.log_to_file("paramiko.log")

# hide main window
root = tkinter.Tk()
root.withdraw()

def check():
    answer = messagebox.askyesno(title="Warning", message="Do you ready to begin the installation?")
    if answer == True:
        print(Fore.BLUE + "Welocme to BP Installer 1.0" + Style.RESET_ALL)
    else:
        sys.exit("Bye!")

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "host_1", "127.0.0.1")
    config.set("Settings", "port_1", "22")
    config.set("Settings", "host_2", "127.0.0.1")
    config.set("Settings", "port_2", "22")
    config.set("Settings", "host_3", "127.0.0.1")
    config.set("Settings", "port_3", "22")
    config.set("Settings", "username", "root")
    config.set("Settings", "password", "22")
    config.set("Settings", "filepath", "/home/")
    config.set("Settings", "localpath", "C://Users//User//Desktop//Build_folder//")
    with open(path, "w") as config_file:
        config.write(config_file)


def crudConfig(path):
    """
    Create, read, update, delete config
    """
    if not os.path.exists(path):
        createConfig(path)
        config = configparser.ConfigParser()
        config.read(path)
        host_1 = input("Type ip address for server_1(press ENTER for localhost): ")
        if host_1 == "":
            config.set("Settings", "host_1", "127.0.0.1")
            print("127.0.0.1")
        else:
            config.set("Settings", "host_1", host_1)
            print(host_1)
        port_1 = input("Type number of port for server_1(press ENTER for 22): ")
        if port_1 == "":
            config.set("Settings", "port_1", "22")
            print("22")
        else:
            config.set("Settings", "port_1", port_1)
            print(port_1)
        host_2 = input("Type ip address for server_2(press ENTER for localhost): ")
        if host_2 == "":
            config.set("Settings", "host_2", "127.0.0.1")
            print("127.0.0.1")
        else:
            config.set("Settings", "host_2", host_2)
            print(host_2)
        port_2 = input("Type number of port for server_2(press ENTER for 22): ")
        if port_2 == "":
            config.set("Settings", "port_2", "22")
            print("22")
        else:
            config.set("Settings", "port_2", port_2)
            print(port_2)
        host_3 = input("Type ip address for server_3(press ENTER for localhost): ")
        if host_3 == "":
            config.set("Settings", "host_3", "127.0.0.1")
            print("22")
        else:
            config.set("Settings", "host_3", host_3)
            print(host_3)
        port_3 = input("Type number of port for server_3(press ENTER for 22): ")
        if port_3 == "":
            config.set("Settings", "port_3", "22")
            print("22")
        else:
            config.set("Settings", "port_3", port_3)
            print(host_3)
        username = input("Type username for all servers(press ENTER for root): ")
        if username == "":
            config.set("Settings", "username", "root")
            print("root")
        else:
            config.set("Settings", "username", username)
            print(username)
        password = input("Type password for your's servers: ")
        config.set("Settings", "password", password)
        filepath = input(
            "Type path where installing packages will be located on remote servers: (press ENTER for /home): ")
        if filepath == "":
            config.set("Settings", "filepath", "/home/")
            print("/home/")
        else:
            config.set("Settings", "filepath", filepath)
            print(filepath)
        localpath = input("Type where installing packages located on local machine: ")
        config.set("Settings", "localpath", localpath)
        print(localpath)
        with open(path, "w") as config_file:
            config.write(config_file)


# select new rpm packeges from localpath
def sel_local_files(localpath):
    files_in_ldir = os.listdir(localpath)
    print(files_in_ldir)


# Regex of desired files for definding specifig old rpm packeges
def find_files(file):
    Regex = re.compile(r'^servicepattern')
    Result = Regex.search(file)
    return Result

def checking_connection(host, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=username, password=password, port=port)
    except:
        messagebox.showerror("Error", f"{host} - Connection can't be established")
        sys.exit("Verify your credentinals")
    print(f"{host} - connection is " + Fore.GREEN + "available" + Style.RESET_ALL)

def check_local_files():
    files_in_local_dir = os.listdir(localpath)
    Regex_check = re.compile(r'.*servicepattern.*')
    if Regex_check.search(str(files_in_local_dir)) == None:
        messagebox.showerror("Error", F"servicepattern packages are absent in {localpath}")
        sys.exit("Bye!")

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
    files_in_local_dir = os.listdir(localpath)
    for file in list_of_files:
        if find_files(file) != None:
            if file not in files_in_local_dir:
                sftp.remove(os.path.join(filepath, file))
                print(Fore.BLUE)
                print(f'{host} The next file: {file} has been removed')
                print(Style.RESET_ALL)
            else:
                print(Fore.CYAN)
                print(f"{host} The next file: {file} is already on the {host}")
                print(Style.RESET_ALL)
    for file in files_in_local_dir:
        if find_files(file) != None:
            if file not in list_of_files:
                print(Fore.YELLOW)
                print(f'{host} Transfering the next file: {file} \n')
                print(Style.RESET_ALL)
                sftp.put(os.path.join(localpath, file), os.path.join(filepath, file))
                print(f'\n {host} The next file has been transfered: {file} \n')
    print(f"{host}: " + Fore.GREEN + " Transfer - Success!" + Style.RESET_ALL)
    # Close
    if sftp: sftp.close()
    if transport: transport.close()


# yum --nogpgcheck localinstall servicepattern-*.rpm -y
def ssh_conection(host, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    print(Fore.YELLOW)
    print(f"{host}: Installation...")
    print(Style.RESET_ALL)
    full_path = os.path.join(filepath,"servicepattern-*.rpm")
    stdin, stdout, stderr = client.exec_command(f'yum --nogpgcheck localinstall {full_path} -y')
    data = stdout.read().decode('UTF-8')
    data_er = stderr.read().decode('UTF-8')
    if bool(data) != False:
        with open(f"{host}_installing.log", "w") as Log_pkg:
            Log_pkg.write(data)
        #TO DO FOR VERIFING errors insight the data
        Regex_error = re.compile(r"error", re.IGNORECASE)
        needed_words = Regex_error.findall(data)
        for word in needed_words:
            new_word = Fore.RED + word + Style.RESET_ALL
            data = Regex_error.sub(new_word, data)
        print(data)
        if Regex_error.search(data) != None:
            answer = messagebox.askyesno(title="Warning!found errors", message="Would you like continue installation?")
            if answer == True:
                print(Fore.BLUE + "Installation is continuing..." + Style.RESET_ALL)
            else:
                sys.exit("Bye!")
    if bool(data_er) == True:
        with open("installing_Log_error.log", "w") as Log_error_pkg:
            Log_error_pkg.write(data_er)
        print(Fore.RED + 'ERROR: ' + Style.RESET_ALL + ' the next happened wrong while installing: \n')
        print(Fore.RED)
        print(data_er)
        print(Style.RESET_ALL)
        messagebox.showerror("Error", " SYS_ERROR : see logs")
        sys.exit("installing_Log_error.log has been created")
    else:
        print(f'{host}:' + Fore.GREEN + ' Installation has been completed! \n' + Style.RESET_ALL)
        client.close()


# DBupdate
def ssh_dbupdate(host, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('/usr/lib/servicepattern/setup/dbUpdate.sh')
    # data = stdout.read() + stderr.read()
    data = stdout.read().decode('UTF-8')
    data_er = stderr.read().decode('UTF-8')
    if bool(data) != False:
        with open("DBupdate.log", "w") as Log_db:
            Log_db.write(data)
        # TO DO FOR VERIFING errors insight the data
        Regex_error = re.compile(r"error", re.IGNORECASE)
        needed_words = Regex_error.findall(data)
        for word in needed_words:
            new_word = Fore.RED + word + Style.RESET_ALL
            data = Regex_error.sub(new_word, data)
        print(data)
        if Regex_error.search(data) != None:
            answer = messagebox.askyesno(title="Warning!found errors", message="Would you like continue installation?")
            if answer == True:
                print(Fore.BLUE + " Installation is continuing..." + Style.RESET_ALL)
            else:
                sys.exit("Bye!")
    if bool(data_er) == True:
        print('ERROR : the next happened wrong while DBupdate: \n')
        print(data_er)
        with open("dbUpdate_error.log", "w") as Log_error_dbUpdate:
            Log_error_pkg.write(data_er)
        messagebox.showerror("Error", "SYS_ERROR: the next happened wrong while DBupdate")
        sys.exit("dbUpdate_error.log has been created")
    else:
        print(f'DBupdate -' + Fore.GREEN + ' SUCCESS \n' + Style.RESET_ALL)
    client.close()


# Restart services
def ssh_restart_service(host, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('/usr/lib/servicepattern/setup/sp_servers.sh restart')
    # data = stdout.read() + stderr.read()
    data = stdout.read().decode('UTF-8')
    data_er = stderr.read().decode('UTF-8')
    if bool(data) != False:
        with open(f"{host}_restart_service.log", "w") as Log_restart:
            Log_restart.write(data)
        # TO DO FOR VERIFING errors insight the data
        Regex_error = re.compile(r"error", re.IGNORECASE)
        needed_words = Regex_error.findall(data)
        for word in needed_words:
            new_word = Fore.RED + word + Style.RESET_ALL
            data = Regex_error.sub(new_word, data)
        print(data)
        if Regex_error.search(data) != None:
            answer = messagebox.askyesno(title="Warning!found errors", message="Would you like continue installation?")
            if answer == True:
                print(Fore.BLUE + " Installation is continuing..." + Style.RESET_ALL)
            else:
                sys.exit("Bye!")
    if bool(data_er) == True:
        print(f'{host}: ' + Fore.GREEN +  'the next happened wrong while restarting services: \n' + Style.RESET_ALL)
        print(data_er)
        with open("restart_error.log", "w") as resstart_error:
            resstart_error.write(data_er)
        messagebox.showerror("Error", "SYS_ERROR : the next happened wrong while restarting services")
        sys.exit("restart_error.log has been created")

    else:
        print(f'{host}:' + Fore.GREEN + ' SUCCESS restart_services has been completed! \n' + Style.RESET_ALL)
    client.close()


def removing_files():
    files_in_local_dir = os.listdir(localpath)
    for file in files_in_local_dir:
        if find_files(file) != None:
            os.remove(os.path.join(localpath, file))
            print(Fore.BLUE)
            print(f'The next file has been removed: {file} from {localpath}')
            print(Style.RESET_ALL)


if __name__ == "__main__":
    path = "BP_installer_config.ini"
    crudConfig(path)
    config = configparser.ConfigParser()
    config.read(path)
    username = config.get("Settings", "username")
    password = config.get("Settings", "password")
    localpath = config.get("Settings", "localpath")
    filepath = config.get("Settings", "filepath")
    check()
    check_local_files()
    checking_connection(config.get("Settings", "host_1"), int(config.get("Settings", "port_1")))
    checking_connection(config.get("Settings", "host_2"), int(config.get("Settings", "port_2")))
    checking_connection(config.get("Settings", "host_3"), int(config.get("Settings", "port_3")))
    connection(config.get("Settings", "host_1"), int(config.get("Settings", "port_1")))
    connection(config.get("Settings", "host_2"), int(config.get("Settings", "port_2")))
    connection(config.get("Settings", "host_3"), int(config.get("Settings", "port_3")))
    print(f"For all servers tranfer " + Fore.GREEN + "COMPLETED \n" + Style.RESET_ALL)
    ssh_conection(config.get("Settings", "host_1"), int(config.get("Settings", "port_1")))
    ssh_conection(config.get("Settings", "host_2"), int(config.get("Settings", "port_2")))
    ssh_conection(config.get("Settings", "host_3"), int(config.get("Settings", "port_3")))
    ssh_dbupdate(config.get("Settings", "host_1"), int(config.get("Settings", "port_1")))
    ssh_restart_service(config.get("Settings", "host_1"), int(config.get("Settings", "port_1")))
    ssh_restart_service(config.get("Settings", "host_2"), int(config.get("Settings", "port_2")))
    ssh_restart_service(config.get("Settings", "host_3"), int(config.get("Settings", "port_3")))
    removing_files()
    messagebox.showinfo("SUCCESS!", "All processes of the installation have been completed")



