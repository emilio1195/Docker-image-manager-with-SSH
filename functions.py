import json
import os, glob, shutil, tempfile
import subprocess
import yaml
from shh_client import Conex_ssh
from commands import *

def create_folder(path):
    #basedir = os.path.dirname(path)  #base path of project
    if not os.path.exists(path):
        print("Creating folder...")
        os.makedirs(path.replace(' ', '_'))
        print("Created Folder: ", path)
    else:
        print("Folder Ok!.")

def write_json(dic_data, path, file_json):
    create_folder(path)
    with open(os.path.join(path, file_json), 'w') as file:
        json.dump(dic_data, file, indent=4, ensure_ascii=False)

def read_json(path, file_json):
    with open(os.path.join(path, file_json)) as file:
        data_json = json.load(file)
    return data_json

def write_env(dic_data, path, file_env):
    create_folder(path)
    with open(os.path.join(path, file_env.replace(' ', '_')), 'w') as file:
        for k, v in dic_data.items():
            file.write(str(k) + '=' + str(v) + '\n')
        file.close()
    print('File .env created!')

def read_env(path, file_env):
    dict_temp = {}
    with open(os.path.join(path, file_env.replace(' ', '_')), 'r') as file:
        for line in file.readlines():
            line = line.strip()
            k = line.split('=')[0]  #vector[0]
            v = line.split('=')[1]  #vector[1]
            dict_temp[k] = v
        file.close()

    return dict_temp  # obj dict

def write_yaml(dic_data, path, file_json):
    with open(os.path.join(path, file_json.replace(' ', '_') + '.yaml'), 'w') as file:
        yaml.dump(dic_data, file)
    print('File .yaml Created!')

def menu_docker(menu_json, basedir_path):
    create_folder(basedir_path)
    docker_data = {}
    for vkey, i in zip(menu_json, range(len(menu_json))):
        value = input(str(i) + "." + vkey + ": ")
        if value == '':
            value = 'null'

        if i == 0:
            name_folder = value
            path = os.path.join(basedir_path, name_folder)
            create_folder(path)
        key = get_key(vkey)
        docker_data[key] = value

    # put function for store
    write_yaml(docker_data, path, name_folder + '_docker-compose')
    write_env(docker_data, path, '.env')

def menu_execute(menu_json, basedir_path):
    dic_commands = {'vedraxx release': vedraxx_release, 'vedraxx install':vedraxx_install,
                    'vedraxx up':vedraxx_up, 'vedraxx down':vedraxx_down,
                    'vedraxx install docker':vedraxx_install_docker, 'vedraxx copy':vedraxx_copy}

    client_ssh = Conex_ssh()
    status_ssh = client_ssh.get_status_conx()
    if status_ssh == False:
        print('Conection Fail!, Try Again')
    else:
        for jkey in menu_json:
            while True:
                print('Return menu input >> back')
                command = input(jkey + ": ")
                if command == 'back':
                    client_ssh.client_ssh_close()
                    break;
                elif command == 'shell':
                    shell_remote(client_ssh)

                numer_spc = command.count(' ')
                command_split = command.rsplit(' ', maxsplit=numer_spc-1)

                command_execute = command_split[0]

                if len(command_split) > 1:
                    source_installation = str(command_split[1]).replace('\\\\','\\')
                else:
                    source_installation = ''

                if len(command_split) > 2:
                    dest_remote_path = command_split[2]
                else:
                    dest_remote_path = ''

                if (command_execute in dic_commands):
                    dic_commands[command_execute](source_installation, client_ssh, dest_remote_path)
                else:
                    print('No exist command!')

def menu_config(menu_json, basedir_path):
    list_options = []
    while True:
        for list_item, i in zip(menu_json['value'], range(len(menu_json))):
            print(list_item + '(%d)' % i)
            list_options.append(list_item)
        option = int(input('Insert option: '))


def Add(data_env, path):
    '''
     if os.path.isfile(os.path.join(path, file_json)):
        config_data = read_env(path, file_json)
    else:
        config_data = {}
    '''

    config_data = {}
    for vkey, i in zip(data_env, range(len(data_env))):
        value = input(vkey + ": ")
        if value == '':
            value = 'null'
        if i == 0:
            name_file_env = value + ".env"

        key = get_key(vkey)
        config_data[key] = value

    write_env(config_data, path, name_file_env)

def Update(data_env, path):
    if not os.path.exists(path):
        print("No exist folder env, please first select the option Add for add a new config")
    else:
        _exit = False
        while not _exit:
            for vkey, i in zip(data_env, range(len(data_env))):

                if i == 0:
                    key = vkey
                    print(key+":")
                    #for config in read_json(path, file_json):
                    with os.scandir(path) as ficheros:
                        ficheros = [fichero.name for fichero in ficheros if fichero.is_file()]
                    for name in ficheros:
                        print("- " + name.split('.')[0])

                else:
                    value = input(vkey + ": ")
                    if i == 1:
                        name_config = value + '.env'
                        Exist_file = ficheros.__contains__(name_config)
                        if Exist_file:
                            config_data = read_env(path, name_config)
                        else:
                            print('Error, Name config incorrect!')
                            break
                    else:
                        key = get_key(vkey)
                        config_data[key] = value

            if(Exist_file):
                write_env(config_data, path, name_config)
                _exit = True

def Delete(data_env, path):
    if not os.path.exists(path):
        print("No exist folder env, please first select the option Add for add a new config")
    else:
        for jkey, i in zip(data_env, range(len(data_env))):

            if i == 0:
                key = jkey
                print(key+":")
                # for config in read_json(path, file_json):
                with os.scandir(path) as ficheros:
                    ficheros = [fichero.name for fichero in ficheros if fichero.is_file()]
                for name in ficheros:
                    print("- " + name.split('.')[0])

            else:
                value = input(jkey + ": ")
                if i == 1:
                    name_config = value + ".env"
                    if ficheros.__contains__(name_config):
                        os.remove(os.path.join(path,name_config))
                        print(f"File {name_config} deleted correctly!")
                    else:
                        print('Error, Name config incorrect!')

def download_git_files_yaml_env(url_gitHib, dst_local):
    #dst = './t'
    temp_dir = tempfile.mkdtemp()
    print(temp_dir)
    args = ['git', 'clone', '--depth=1', url_gitHib, temp_dir]
    res = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, _error = res.communicate()

    if not _error:
        # print(output)
        # Copy desired file from temporary dir
        # temp_dir = os.path.join(temp_dir, 'docs')
        files_yml = glob.glob1(temp_dir, '*.yaml')
        files_env = glob.glob1(temp_dir, '*.env')
        for i in files_yml:
            print('Moving file >> ', i)
            shutil.move(os.path.join(temp_dir, i), os.path.join(dst_local, i))
        for k in files_env:
            print('Moving file >> ', k)
            shutil.move(os.path.join(temp_dir, k), os.path.join(dst_local, k))
        # Remove temporary dir
        shutil.rmtree(temp_dir)
    else:
        print(_error)

def get_key(vkey):
    if vkey == 'Configuration Name':
        return 'NAME_CONF'
    elif vkey == 'Add remote server ip':
        return 'SERVER_IP'
    elif vkey == 'Add remote port':
        return 'SERVER_PORT'
    elif vkey == 'Add registry(optional)':
        return 'REGISTRY'
    elif vkey == 'Add registry username(optional)':
        return 'USERNAME'
    elif vkey == 'Add registry password(optional)':
        return 'PASSWORD'
    elif vkey == 'Installation name':
        return 'INSTALL_NAME'
    elif vkey == 'Add engine?(optional) yes/not':
        return 'ADD_ENGINE'
    elif vkey == 'Add transit-random-generator?(optional)':
        return 'TRANSIT_RANDOM_GENERATOR'
    elif vkey == 'Add transit-permit-ext?(optional)':
        return 'TRANSIT_PERMIT_EXT'
    elif vkey == 'Digit maintainer email':
        return 'DIGIT_MAINTAINER_EMAIL'
    elif vkey == 'Host/Ip Address':
        return 'HOST_IP'
    elif vkey == 'Digits version(lastest or RC)':
        return 'DIGIT_VERSION'




'''
def Add(data_json, path, file_json):
    if os.path.isfile(os.path.join(path, file_json)):
        config = read_env(path, file_json)
    else:
        config = {}

    config_data = {}
    key = ''
    for jkey, i in zip(data_json, range(len(data_json))):
        value = input(jkey + ": ")
        
        if i == 0:
            key = value
            config[key] = [] #Json name config with Object
        else:
            config_data[jkey] = value

    config[key].append(config_data)
    write_env(config, path, file_json)
'''