import json
import os
import data

menu_json = data.file_menu_json

from functions import menu_docker, menu_execute, menu_config, Add, Update, Delete

list_functions = [menu_docker, menu_execute, menu_config]
list_functions_config = [Add, Update, Delete]
list_txt_config = ['Add', 'Update', 'Delete']

with open(os.path.join('.',data.name_folder_json, menu_json)) as file:
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
            option = int(input('Insert option: '))

            for item in menu[list_options[option]]:
                print('\n**_______ %s Menu________**' % list_options[option])
                for num_item, i in zip(item, range(len(item))):
                    if (item[num_item]['value'] ==''):
                        list_functions[option](item[num_item]['List_items'])
                    else:
                        print(item[num_item]['value'] + '(%d)' % i)
                        list_option_config.append(item[num_item]['value'])

                if (item[num_item]['value'] != ''):
                    option = int(input('Insert option: '))
                    if option < len(list_txt_config):
                        print('\n**_______ %s Menu________**' % list_txt_config[option])
                        list_functions_config[option](item['item'+str(option+1)]['List_items'])

                    else: break

