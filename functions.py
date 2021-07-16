import json
import os, glob, shutil, tempfile
import subprocess
import yaml
import dataV

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

def read_yaml(path_folder_, name_File):
    path_file = os.path.join(path_folder_, name_File + '.yaml')
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
    path_folder_compose = os.path.join('.', dataV.name_folder_compose)
    create_folder(path_folder_compose)
    dic_env = {}
    docker_data = {
                    'version': '3.7',
                    'services': {}
                  }
    dic_services = {}
    for vkey, i in zip(menu_json, range(len(menu_json))):
        value = input(str(i) + "." + vkey + ": ")
        if value == 'back':
            break

        key = get_key(vkey)
        if value == '':
            value = 'null'

        if i == 0:
            name_folder = value
            path = os.path.join(path_folder_compose, name_folder)
            create_folder(path)
            download_git_files_yaml_env(dataV.github_repo, path)
            dic_env = read_env(path)
            #store_env2json(name_folder, path)
            docker_data_tmp = read_yaml(path, name_folder+'_docker-compose')
            if bool(docker_data_tmp):
                docker_data = docker_data_tmp
                dic_services = docker_data['services']
            else:
                dic_services = docker_data['services']
        else:
            if (value == 'yes') | (value == 'y'):
                if "engine" in vkey:
                    dic_services["engine"] = ["#TODO"]
                elif "random-generator" in vkey:
                    dic_services["random-generator"] = ["#TODO"]
                elif "permit" in vkey:
                    dic_services['permit-ext'] = ["#TODO"]
                docker_data['services'] = dic_services

            if  ('email' in vkey) | ('Host/Ip' in vkey) | ('version' in vkey):
                if (value != 'null'):
                    dic_env[key] = value

                dic_env[name_folder + '_' + key] = dic_env.pop(key)

    if value != 'back':
        # put function for store
        write_yaml(docker_data, path, name_folder + '_docker-compose')
        write_env(dic_env, path)
        #if exist config for this installation in the file json, will be stored, else will be ignored
        store_env_compose(name_folder, path)

#store config from json array to env in folder name install compose
def store_env_compose(name_install_compose, path_folder_install_compose = ''):
    if path_folder_install_compose == '':
        path_folder_install_compose = os.path.join('.', dataV.name_folder_compose, name_install_compose)
    if os. path.isdir(path_folder_install_compose):
        if os.path.isfile(os.path.join(path_folder_install_compose, '.env')):
            dic_git = read_env(path_folder_install_compose)
        else:
            dic_git = {}

        path_json = os.path.join(".", dataV.name_folder_json)
        if os.path.isfile(os.path.join(path_json, dataV.file_config_json)):
            file_json = read_json(path_json, dataV.file_config_json)
            if name_install_compose in file_json.keys():
                data_env = file_json[name_install_compose]
                dic_git.update(data_env)
                write_env(dic_git, path_folder_install_compose)
            else:
                print("No exist this name config: {} in the file Json, for store in format .env".format(name_install_compose))

#store env downloaded to file config.json, where are all configs have been store beforely
def store_env2json(name_install_compose, path_folder_install_compose):
    path_json = os.path.join(".", dataV.name_folder_json)
    if os.path.isfile(os.path.join(path_folder_install_compose, '.env')):
        data_env = read_env(path_folder_install_compose)
        if os.path.isfile(os.path.join(path_json, dataV.file_config_json)):
            data_json = read_json(path_json, dataV.file_config_json)
            if not name_install_compose in data_json.keys():
                data_json[name_install_compose] = data_env
                write_json(data_json, path_json, dataV.file_config_json)
            else:
                print("No exist this name config: {}, for store in format .env".format(name_install_compose))

def menu_execute(menu_json):
    dic_commands = {'vedraxx release': vedraxx_release, 'vedraxx install':vedraxx_install,
                    'vedraxx up':vedraxx_up, 'vedraxx down':vedraxx_down,
                    'vedraxx install docker':vedraxx_install_docker, 'vedraxx copy':vedraxx_copy}

    client_ssh = ShellHandler(dataV.HOST, dataV.USER, dataV.PASS)
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
                elif command == 'shell2':
                    while True:
                        cmd = input("cmd shell2 >> ")
                        if cmd == 'back':
                            print('Shell2 closed!')
                            break
                        else:
                            control_cmd_interactive([cmd], client_ssh)

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
    folder_json = os.path.join(".", dataV.name_folder_json)
    if os.path.isfile(os.path.join(folder_json, dataV.file_config_json)):
        config_array_obj = read_json(folder_json, dataV.file_config_json)
    else:
        config_array_obj = {}

    dic_primitivesJson = {}
    key = ''
    for jkey, i in zip(data_json, range(len(data_json))):
        value = input(jkey + ": ")

        if i == 0:
            while True:
                if not value in config_array_obj:
                    key_name = value
                    config_array_obj[key_name] = {}  # Json name config with Object
                    break
                else:
                    print("This name already exist, try with other name.\n")
                    value = input(jkey + ": ")

        else:
            key = key_name + '_' + get_key(jkey)
            dic_primitivesJson[key] = value

    config_array_obj[key_name] = dic_primitivesJson
    write_json(config_array_obj, folder_json, dataV.file_config_json)
    #read if exist file .env in the folder nameConfig and read the json key, then join data for update .env and store
    store_env_compose(key_name)

def Update(data_json):
    folder_json = os.path.join(".", dataV.name_folder_json)
    if os.path.isfile(os.path.join(folder_json, dataV.file_config_json)):
        config_array_obj = read_json(folder_json, dataV.file_config_json)
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
                    while name_config != 'back':
                        if name_config in config_array_obj.keys():
                            config_data = config_array_obj[name_config]
                            break
                        else:
                            print('Error, Name config incorrect, try again!')
                            name_config = input(jkey + ": ")
                            value = name_config

                else:
                    if value == 'back':
                        break
                    else:
                        key = name_config + '_' + get_key(jkey)
                        config_data[key] = value

                if value == 'back':
                    break

        if value == 'back':
            pass
        else:
            config_array_obj[name_config] = config_data
            write_json(config_array_obj, folder_json, dataV.file_config_json)
            # read if exist file .env in the folder nameConfig and read the json key, then join data for update .env and store
            store_env_compose(name_config)
    else:
        print("No exist file: ", dataV.file_config_json)

def Delete(data_json):
    path_folder_env = os.path.join('.', dataV.name_folder_compose)
    folder_json = os.path.join(".", dataV.name_folder_json)
    if os.path.isfile(os.path.join(folder_json, dataV.file_config_json)):
        config_array_obj = read_json(folder_json, dataV.file_config_json)

        for jkey, i in zip(data_json, range(len(data_json))):
            if i == 0:
                print(jkey + ":")
                for key in config_array_obj.keys():
                    print("- ", key)
            else:
                value = input(jkey + ": ")
                name_config = value

                while name_config != 'back':
                    if name_config in config_array_obj.keys():
                        try:
                            del config_array_obj[name_config]
                            path_folder_env = os.path.join(path_folder_env, name_config, ".env")
                            if os.path.isfile(path_folder_env):
                                os.remove(path_folder_env)
                            print("Config: {}, have been deleted".format(name_config))
                        except:
                            print('Error, Name config incorrect, try again!')

                        break
                    else:
                        print('Error, Name config incorrect, try again!')
                        name_config = input(jkey + ": ")
        if value == 'back':
            pass
        else:
            write_json(config_array_obj, folder_json, dataV.file_config_json)

    else:
        print("No exist file: ", dataV.file_config_json)


def download_git_files_yaml_env(url_gitHib_repo, path_store, folder_repo = ''):
    #dst = './t'
    path_storage = os.path.join('.', dataV.name_folder_compose)
    if not os.path.isfile(os.path.join(path_storage,dataV.name_file_git_yaml)) & os.path.isfile(os.path.join(path_storage, '.env')):
        temp_dir = tempfile.mkdtemp()
        print(temp_dir)
        args = ['git', 'clone', '--depth=1', url_gitHib_repo, temp_dir]
        res = subprocess.Popen(args, stdout=subprocess.PIPE)
        output, _error = res.communicate()
        Exist = False
    else:
        temp_dir = path_storage
        Exist = True

    # print(output)
    # Copy desired file from temporary dir
    files_yml = glob.glob1(os.path.join(temp_dir, folder_repo), dataV.name_file_git_yaml)
    files_env = glob.glob1(os.path.join(temp_dir, folder_repo), '.env')

    if Exist:
        if not os.path.isfile( os.path.join(path_store, path_store.rsplit('\\', maxsplit=1)[1] +'_docker-compose.yaml')):
            for file in files_yml:
                print('Copying file >> ', file)
                shutil.copy(os.path.join(temp_dir, file), os.path.join(path_store, file))
                os.rename(os.path.join(path_store, file), os.path.join(path_store, path_store.rsplit('\\', maxsplit=1)[1] +'_docker-compose.yaml'))

        if not os.path.isfile(os.path.join(path_store, '.env')):
            for file in files_env:
                print('Copying file >> ', file)
                shutil.copy(os.path.join(temp_dir, file), os.path.join(path_store, file))
    else:
        if not _error:
            for file in files_yml:
                print('Moving file >> ', file)
                shutil.move(os.path.join(temp_dir, folder_repo, file), os.path.join(path_storage, file))
                print('Copying file >> ', file)
                shutil.copy(os.path.join(path_storage, file), os.path.join(path_store, file))
                os.rename(os.path.join(path_store, file), os.path.join(path_store, path_store.rsplit('\\', maxsplit=1)[1] +'_docker-compose.yaml'))
            for file in files_env:
                print('Moving file >> ', file)
                shutil.move(os.path.join(temp_dir, folder_repo, file), os.path.join(path_storage, file))
                print('Copying file >> ', file)
                shutil.copy(os.path.join(path_storage, file), os.path.join(path_store, file))

        else:
            print(_error)

    # Remove temporary dir
    # shutil.rmtree(temp_dir)

def get_key(vkey):
    if(os.path.isfile(os.path.join('.',dataV.name_folder_json, dataV.file_keys_env_json))):
        dic_keys = read_json(dataV.name_folder_json, dataV.file_keys_env_json)
        for obj_json in dic_keys:
            if vkey in obj_json.keys():
                return obj_json[vkey]
        return ''
    else: return ''