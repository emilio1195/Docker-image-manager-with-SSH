import json
import os
from functions import create_folder
import dataV
item1 = 'Menu_Principal'
menu = {item1:[]}

list_items_Docker = ['Installation name', 'Add engine?(optional) yes/not',
                     'Add transit-random-generator?(optional)', 'Add transit-permit-ext?(optional)',
                     'Digit maintainer email', 'Host/Ip Address', 'Digits version(lastest or RC)']

list_items_Add = ['Configuration Name', 'Add remote server ip', 'Add remote port', 'Add registry(optional)',
              'Add registry username(optional)', 'Add registry password(optional)']

list_items_Update = ['List of all configuration availables', 'Enter the configuration name', 'Add remote port',
              'Add registry(optional)', 'Add registry username(optional)', 'Add registry password(optional)']

list_items_DelConfig = ['List of all configuration availables', 'Enter the configuration name to delete']

keys_env_Docker = {list_items_Docker[4]:'MAINTAINER_EMAIL', list_items_Docker[5]:'SERVER_IP', list_items_Docker[6]:'VERSION'}

keys_env_Config = {list_items_Add[1]:'SERVER_IP', list_items_Add[2]:'SERVER_PORT', list_items_Add[3]:'REGISTRY',
                   list_items_Add[4]:'USER_REGISTRY', list_items_Add[5]:'PASS_REGISTRY'}

dic_keys_items = [keys_env_Docker, keys_env_Config]

menu_main = {'Docker-compose':[
                                {'item1': {
                                            'value': '',
                                            'List_items': list_items_Docker
                                          }
                                }],
             'Execute command':[
                                {'item1': {
                                            'value': '',
                                            'List_items': [">>Digit Command"]
                                          }
                                }],
             'Configuration':[]
            }

menu_Config = {'Add': list_items_Add,
              'Update': list_items_Update,
              'Delete configuration': list_items_DelConfig,
              'Back': []}
idx = 0
for item in menu_Config:
    idx += 1
    menu_main['Configuration'].append({

        'item'+str(idx): {
                            'value': item,
                            'List_items': menu_Config[item]
                        }
    })

menu[item1].append(menu_main)
dir = os.path.join('.', dataV.name_folder_json)
create_folder(dir)
with open(os.path.join(dir, dataV.file_menu_json), 'w') as file:
    json.dump(menu, file, indent=4, ensure_ascii=False)
print('File {}, Created!'.format(dataV.file_menu_json))

with open(os.path.join(dir, dataV.file_keys_env_json), 'w') as file:
    json.dump(dic_keys_items, file, indent=4, ensure_ascii=False)
print('File {}, Created!'.format(dataV.file_keys_env_json))

