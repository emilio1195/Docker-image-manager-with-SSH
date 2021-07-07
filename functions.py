import json
import os, glob, shutil, tempfile
import subprocess
import yaml
import data

from shellhandler import ShellHandler
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

def write_env(dic_data, path):
    create_folder(path)
    with open(os.path.join(path, '.env'), 'w') as file:
        for k, v in dic_data.items():
            file.write(str(k) + '=' + str(v) + '\n')
        file.close()
    print('File .env created!')

def read_env(path):
    dict_temp = {}
    with open(os.path.join(path, '.env'), 'r') as file:
        for line in file.readlines():
            line = line.strip()
            k = line.split('=')[0]  #vector[0]
            v = line.split('=')[1]  #vector[1]
            dict_temp[k] = v
        file.close()

    return dict_temp  # obj dict

def read_yaml(path_folder, name_File):
    path_file = os.path.join(path_folder, name_File + '.yaml')
    if os.path.isfile(path_file):
        with open(path_file, 'r') as file:
            try:
                data_yaml = yaml.full_load(file)
            except:
                data_yaml={}

        return data_yaml
    else:
        return {}

def write_yaml(dic_data, path, file_json):
    with open(os.path.join(path, file_json.replace(' ', '_') + '.yaml'), 'w') as file:
        yaml.dump(dic_data, file, sort_keys=False)
    print('File .yaml Created!')

def menu_docker(menu_json):
    path_folder_compose = os.path.join('.', data.name_folder_compose)
    create_folder(path_folder_compose)
    docker_data = {
                    'version': '3.7',
                    'services': {},
                    'networks':{}
                  }
    dic_services = {}
    for vkey, i in zip(menu_json, range(len(menu_json))):
        value = input(str(i) + "." + vkey + ": ")
        if value == '':
            value = 'null'

        if i == 0:
            name_folder = value
            path = os.path.join(path_folder_compose, name_folder)
            create_folder(path)
            if not os.path.isfile(os.path.join(path, name_folder+'_docker-compose.yaml')):
                download_git_files_yaml_env(data.github_repo, path, name_folder)
            store_env2json(name_folder, path)
            docker_data_tmp = read_yaml(path, name_folder+'_docker-compose')
            if bool(docker_data_tmp):
                docker_data = docker_data_tmp
                dic_services = docker_data['services']
            else:
                dic_services = docker_data['services']

        if value == 'yes':
            if "engine" in vkey:
                dic_services["engine"] = "#TODO"
            elif "random-generator" in vkey:
                dic_services["random-generator"] = "#TODO"
            elif "permit" in vkey:
                dic_services['permit-ext'] = "#TODO"
            docker_data['services'] = dic_services

        if "Host/Ip" in vkey:
            docker_data["networks"] = {'frontend': {'ipam':{'config':[{"subnet":value}]}}}

    # put function for store
    write_yaml(docker_data, path, name_folder + '_docker-compose')
    store_env_compose(name_folder, path)

#store config from json array to env in folder name install compose
def store_env_compose(name_install_compose, path_folder_install_compose):
    path_json = os.path.join(".", data.name_folder_json)
    if os.path.isfile(os.path.join(path_json, data.file_config_json)):
        file_json = read_json(path_json, data.file_config_json)
        if name_install_compose in file_json.keys():
            data_env = file_json[name_install_compose]
            write_env(data_env, path_folder_install_compose)
        else:
            print("No exist this name config: {}, for store in format .env".format(name_install_compose))

#store env downloaded to file config.json, where are all configs have been store beforely
def store_env2json(name_install_compose, path_folder_install_compose):
    path_json = os.path.join(".", data.name_folder_json)
    if os.path.isfile(os.path.join(path_folder_install_compose, '.env')):
        data_env = read_env(path_folder_install_compose)
        if os.path.isfile(os.path.join(path_json, data.file_config_json)):
            data_json = read_json(path_json, data.file_config_json)
            if not name_install_compose in data_json.keys():
                data_json[name_install_compose] = data_env
                write_json(data_json, path_json, data.file_config_json)
            else:
                print("No exist this name config: {}, for store in format .env".format(name_install_compose))

def menu_execute(menu_json):
    dic_commands = {'vedraxx release': vedraxx_release, 'vedraxx install':vedraxx_install,
                    'vedraxx up':vedraxx_up, 'vedraxx down':vedraxx_down,
                    'vedraxx install docker':vedraxx_install_docker, 'vedraxx copy':vedraxx_copy}

    client_ssh = ShellHandler(data.HOST, data.USER, data.PASS)
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
                    break
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

def menu_config(menu_json):
    list_options = []
    while True:
        for list_item, i in zip(menu_json['value'], range(len(menu_json))):
            print(list_item + '(%d)' % i)
            list_options.append(list_item)
        option = int(input('Insert option: '))


def Add(data_json):
    folder_json = os.path.join(".", data.name_folder_json)
    if os.path.isfile(os.path.join(folder_json, data.file_config_json)):
        config_array_obj = read_json(folder_json, data.file_config_json)
    else:
        config_array_obj = {}

    dic_primitivesJson = {}
    key = ''
    for jkey, i in zip(data_json, range(len(data_json))):
        value = input(jkey + ": ")

        if i == 0:
            while True:
                if not value in config_array_obj:
                    key = value
                    config_array_obj[key] = {}  # Json name config with Object
                    break
                else:
                    print("This name already exist, try with other name.\n")
                    value = input(jkey + ": ")

        else:
            dic_primitivesJson[jkey] = value

    config_array_obj[key] = dic_primitivesJson
    write_json(config_array_obj, folder_json, data.file_config_json)


def Update(data_json):
    folder_json = os.path.join(".", data.name_folder_json)
    if os.path.isfile(os.path.join(folder_json, data.file_config_json)):
        config_array_obj = read_json(folder_json, data.file_config_json)
        dic_primitivesJson = {}
        key = ''
        for jkey, i in zip(data_json, range(len(data_json))):
            if i == 0:
                print(jkey + ":")
                for key in config_array_obj.keys():
                    print("- ", key)
            else:
                value = input(jkey + ": ")
                if i == 1:
                    name_config = value
                    while True:
                        if name_config in config_array_obj.keys():
                            config_data = config_array_obj[name_config]
                            break
                        else:
                            print('Error, Name config incorrect, try again!')
                            name_config = input(jkey + ": ")
                else:
                    #key = get_key(jkey)
                    config_data[jkey] = value

        config_array_obj[name_config] = config_data
        write_json(config_array_obj, folder_json, data.file_config_json)

    else:
        print("No exist file: ", data.file_config_json)

def Delete(data_json):
    folder_json = os.path.join(".", data.name_folder_json)
    if os.path.isfile(os.path.join(folder_json, data.file_config_json)):
        config_array_obj = read_json(folder_json, data.file_config_json)

        for jkey, i in zip(data_json, range(len(data_json))):
            if i == 0:
                print(jkey + ":")
                for key in config_array_obj.keys():
                    print("- ", key)
            else:
                value = input(jkey + ": ")
                name_config = value
                while True:
                    if name_config in config_array_obj.keys():
                        del config_array_obj[name_config]
                        print("Config: {}, have been delete".format(name_config))
                        break
                    else:
                        print('Error, Name config incorrect, try again!')
                        name_config = input(jkey + ": ")

        write_json(config_array_obj, folder_json, data.file_config_json)
    else:
        print("No exist file: ", data.file_config_json)

def download_git_files_yaml_env(url_gitHib, path, name_intall_compose):
    #dst = './t'
    temp_dir = tempfile.mkdtemp()
    print(temp_dir)
    args = ['git', 'clone', '--depth=1', url_gitHib, temp_dir]
    res = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, _error = res.communicate()

    if not _error:
        # print(output)
        # Copy desired file from temporary dir

        files_yml = glob.glob1(os.path.join(temp_dir, name_intall_compose), '*.yaml')
        files_env = glob.glob1(os.path.join(temp_dir, name_intall_compose), '*.env')
        for file in files_yml:
            print('Moving file >> ', file)
            shutil.move(os.path.join(temp_dir, name_intall_compose, file), os.path.join(path, file))
        for file in files_env:
            print('Moving file >> ', file)
            shutil.move(os.path.join(temp_dir, name_intall_compose, file), os.path.join(path, file))
        # Remove temporary dir
        #shutil.rmtree(temp_dir)
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
        return 'MAINTAINER_EMAIL'
    elif vkey == 'Host/Ip Address':
        return 'HOST_IP'
    elif vkey == 'Digits version(lastest or RC)':
        return 'VERSION'




'''
def Add(data_env, path):
    ''
     if os.path.isfile(os.path.join(path, file_json)):
        config_data = read_env(path, file_json)
    else:
        config_data = {}
    ''

    config_data = {}
    for vkey, i in zip(data_env, range(len(data_env))):
        value = input(vkey + ": ")
        if value == '':
            value = 'null'
        if i == 0:
            name_file_env = value

        key = get_key(vkey)
        config_data[key] = value

    write_env(config_data, path, name_file_env)
'''