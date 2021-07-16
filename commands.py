import sys
import time

import paramiko
import os
from pathlib import Path
import json
import requests
import dataV
def clean_buffer(client_ssh, delay=5):
    client_ssh.command_client('clear')
def control_cmd_interactive(list_commands, client_ssh, delay=0.5):
    key = ''
    #clean_buffer(client_ssh)
    for command in list_commands:
        cont = 0
        while True:
            key = client_ssh.execute(command)

            if key.rstrip(' ') != '$':
                command = ''
                time.sleep(delay)

            if key.rstrip(' ') == '$':
                break
            elif (key.rstrip(' ') == '') & (cont > 2):
                print("\nFinish command.\n")
                break
            cont += 1
        client_ssh.invoke_newShell()

def vedraxx_install_docker(client_ssh):
    list_commands = ['sudo curl -fsSL https://get.docker.com | sh',
                     'sudo service docker start',
                     'sudo docker run hello-world',
                     'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose',
                     'sudo chmod +x /usr/local/bin/docker-compose']

    control_cmd_interactive(list_commands, client_ssh, delay=30)

def vedraxx_release(i='', l='', n=''):
    #show versions
    url_registry = dataV.registry.rstrip('/')
    # url_registry = input('Url Registry where are the images '
    #                     '(example: https://registry.domain/):\n>> ').rstrip('/')

    solditems = requests.get(url_registry + '/_catalog')
    data = solditems.json()
    for name_image in data['repositories']:
        name = name_image
        print('\n> image: ', name)
        if not "/" in name:
            solditems = requests.get(url_registry + '/' + name + '/tags/list')
            data_tags = solditems.json()
            for tags in data_tags['tags']:
                print(' - ', tags)

def vedraxx_up(install_name, client_ssh, n=''):
    #copy folder to remote folder
    vedraxx_install(install_name, client_ssh)
    path_server = get_path_server_remote(client_ssh)
    path = os.path.join(path_server, install_name, install_name +'_docker-compose.yaml').replace('\\', '/')
    print('sudo docker-compose up, wait...')
    list_commands = ['sudo docker-compose -f {name} up'.format(name=path)]
    control_cmd_interactive(list_commands, client_ssh)

def vedraxx_down(install_name, client_ssh, n=''):
    #execute command in remote server
    path_server = get_path_server_remote(client_ssh)
    path = os.path.join(path_server, install_name, install_name + '_docker-compose.yaml').replace('\\', '/')
    list_commands = ['sudo docker-compose -f {name} down'.format(name=path)]
    print('sudo docker-compose down, wait...')
    '''
    list_commands = ['cd {path}'.format(path=os.path.join(path_server, install_name).replace('\\', '/')),
                     'sudo docker-compose -f {name}_docker-compose.yaml down'.format(name=install_name),
                     'cd /home/']
    '''
    control_cmd_interactive(list_commands, client_ssh)

def vedraxx_install(name_folder, client_ssh, n=''):
    #install docker & docker-compose in the server
    # install docker & docker-compose in the server

    if name_folder == 'docker':
        vedraxx_install_docker(client_ssh)
    else:
        path_dest_remote = get_path_server_remote(client_ssh)
        path_folder_ = Path(os.path.join('.', dataV.name_folder_compose, name_folder)).parent.absolute()
        ftp_client = client_ssh.open_sftp()
        put_dir(path_folder_, path_dest_remote, name_folder, ftp_client)
        client_ssh.sftp_close()

def vedraxx_copy(path_folder_local, client_ssh, path_dest_remote):
    #copy all content of the local folder to remote server in specific folder.
    #path_dest_remote = input('Insert path from remote server where it will be copy\n(Example: /home/user/folder_dest/) >> ')
    path_folder_local =  path_folder_local.rstrip('\\').rstrip('/')
    if path_folder_local.count('\\') > 0:
        arr_path = path_folder_local.rsplit('\\', maxsplit=1)
    elif path_folder_local.count('/') > 0:
        arr_path = path_folder_local.rsplit('/', maxsplit=1)
    path_source = arr_path[0]
    name_folder_local = arr_path[1]
    ftp_client = client_ssh.open_sftp()
    put_dir(path_source, path_dest_remote, name_folder_local, ftp_client)
    print("Copied Succesful!")
    client_ssh.sftp_close()


def normalize_path(path_dest_remote):
    if len(path_dest_remote) > 1 & path_dest_remote[-1:] == '/':
        return path_dest_remote
    else:
        return path_dest_remote +'/'

def get_name_folder():
    while True:
        folder = input("Name Folder>> ")
        if os.path.isdir(folder):
            return folder
        else:
            print('No exist folder, try again!')


def put_dir(source, dest, name_folder, sftp):
    source = os.path.expandvars(source).rstrip('\\').rstrip('/')
    dest = os.path.expandvars(dest).rstrip('\\').rstrip('/')

    if os.path.isdir(os.path.join(source, name_folder)):
        path_newFolder = os.path.join(dest, name_folder).replace('\\', '/').replace(' ', '_')
        destPathExists = create_folder(sftp, path_newFolder) #create folder in path remote server

        if destPathExists == False:
            print('$$ Error to create dir: {} into server, Try Again!'.format(path_newFolder))
        else:
            for root, dirs, files in os.walk(os.path.join(source, name_folder), topdown=True):
                for name in files:
                    file_path_local = os.path.join(root, name).replace('/', '\\')
                    file_path_remote = os.path.join(dest, ''.join(root.rsplit(source))[1:], name)\
                                                .replace('\\','/').replace(' ','_')
                    print("Copying file... >>\nlocal: {} to\nremote: {}".format(file_path_local, file_path_remote))
                    with TqdmWrap(ascii=True, unit='b', unit_scale=True) as pbar:
                        # Call paramiko with tqdm callback
                        sftp.put(file_path_local, file_path_remote, callback=pbar.viewBar)
                for name in dirs:
                    folder_path_remote = os.path.join(dest, ''.join(root.rsplit(source))[1:], name)\
                                                    .replace('\\', '/').replace(' ', '_')
                    destPathExists = create_folder(sftp, folder_path_remote)  # create folder in path remote server
                    if destPathExists == False:
                        print('Error to create dir: {}\n Try Again!'.format(folder_path_remote))
                    else:
                        print("Created sub-folder... >> ", folder_path_remote)

            print("Copied Succesful in path_remote >> ", path_newFolder)
    else:
        print('Direcotry no exist!')


def get_path_server_remote(client_ssh):
    list_result = client_ssh.command_client('pwd')
    return (list_result[0]).rstrip('\r')

def create_folder(ftp_client, path_newFolder):
    try:
        print("Creating folder... >> ", path_newFolder)
        ftp_client.mkdir(path_newFolder)
        destPathExists = True
    except Exception as e:
        try:
            filestat = ftp_client.stat(path_newFolder)
            destPathExists = True
        except Exception as e:
            destPathExists = False
            print(e)
    return destPathExists

def shell_remote(client_ssh):
    while True:
        cmd = input("cmd shell >> ")
        if cmd == 'back':
            print('Shell closed!')
            break
        else:
            client_ssh.command_client(cmd)


try:
    from tqdm import tqdm
except ImportError:
    class TqdmWrap(object):
        # tqdm not installed - construct and return dummy/basic versions
        def __init__(self, *a, **k):
            pass

        def viewBar(self, a, b):
            # original version
            res = a / int(b) * 100
            sys.stdout.write('\rComplete precent: %.2f %%' % (res))
            sys.stdout.flush()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False
else:
    class TqdmWrap(tqdm):
        def viewBar(self, a, b):
            self.total = int(b)
            self.update(int(a - self.n))  # update pbar with increment