import json
import os
import dataV

menu_json = dataV.file_menu_json

from functions import menu_docker, menu_execute, menu_config, Add, Update, Delete

list_functions = [menu_docker, menu_execute, menu_config]
list_functions_config = [Add, Update, Delete]
list_txt_config = ['Add', 'Update', 'Delete']

with open(os.path.join('.', dataV.name_folder_json, menu_json)) as file:
    data_menu = json.load(file)
    list_options=[]
    list_items = []
    list_option_config = []
    while True:
        for menu in data_menu['Menu_Principal']:
            print('\n**_______ Main Menu ________**')
            for list_item, i in zip(menu, range(len(menu))):
                print(list_item + '(%d)'% i)
                list_options.append(list_item)

            while True:
                try:
                    option = int(input('Insert option: '))
                    if option > 2:
                        print('Error option, try again!')
                    else: break
                except:
                    print('Input a number, please!')
            while True:
                print('\n**_______ %s Menu________**' % list_options[option])
                submenu = menu[list_options[option]]
                for item, num_item in zip(submenu, range(1,len(submenu)+1)):
                    if item['item'+str(num_item)]['value'] == '':
                        list_functions[option](item['item'+str(num_item)]['List_items'])
                    else:
                        print(item['item'+str(num_item)]['value'] + '(%d)' % num_item)
                        list_option_config.append(item['item'+str(num_item)]['value'])

                if (item['item'+str(num_item)]['value'] != ''):
                    try:
                        option_submenu = int(input('Insert option: ')) - 1
                        if option_submenu < len(list_txt_config):
                            print('\n**_______ %s Menu________**' % list_txt_config[option_submenu])
                            list_functions_config[option_submenu](submenu[option_submenu]['item'+str(option_submenu+1)]['List_items'])
                        else: break
                    except:
                        print('Input a number')
                else:
                    break
