import json
import os
from functions import create_folder
import data
item1 = 'Menu_Principal'
menu = {item1:[]}

list_items = ['Docker-compose', 'Execute command', 'Configuration']
menu_items = {list_items[0]:[], list_items[1]:[], list_items[2]:[]}

list_items_Docker = ['Installation name', 'Add engine?(optional) yes/not',
                     'Add transit-random-generator?(optional)', 'Add transit-permit-ext?(optional)',
                     'Digit maintainer email', 'Host/Ip Address', 'Digits version(lastest or RC)']
list_items_Config = ['Add', 'Update', 'Delete configuration', 'Back']
list_items_Add = ['Configuration Name', 'Add remote server ip', 'Add remote port', 'Add registry(optional)',
              'Add registry username(optional)', 'Add registry password(optional)']
list_items_Update = ['List of all configuration availables', 'Enter the configuration name', 'Add remote port',
              'Add registry(optional)', 'Add registry username(optional)', 'Add registry password(optional)']
list_items_DelConfig = ['List of all configuration availables', 'Enter the configuration name to delete']

menu_items[list_items[0]].append({
    'item1':{
            'value':'',
            'List_items':list_items_Docker
            }
    })
menu_items[list_items[1]].append({
    'item1':{
            'value':'',
            'List_items':['>>Digit Command']
            }
    })
menu_items[list_items[2]].append({
    'item1':{
        'value':list_items_Config[0],
        'List_items':list_items_Add
    },
    'item2':{
            'value':list_items_Config[1],
            'List_items':list_items_Update
        },
    'item3':{
            'value':list_items_Config[2],
            'List_items':list_items_DelConfig
        },
    'item4':{
            'value':list_items_Config[3],
            'List_items':[]
        }
    })

menu[item1].append(menu_items)
dir = os.path.join('.', data.name_folder_json)
create_folder(dir)
with open(os.path.join(dir, data.file_menu_json), 'w') as file:
    json.dump(menu, file, indent=4, ensure_ascii=False)
