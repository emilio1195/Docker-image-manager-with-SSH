import os
from pathlib import Path
#source = 'C:\\Users\\gta20\\Documents\\ProjectsPyCharm\\Code_Menu'
import os, glob
import shutil
import tempfile
import subprocess
import data
#from functions import read_json
path = os.path.join('.',data.name_folder_json)
#js = read_json(path, data.file_config_json)

if ('sd' == 'sd') & (3 == 3):
    print('ok')


import yaml

with open(r'C:\Users\gta20\Documents\ProjectsPyCharm\Code_Menu (2)\Code_Menu\awesome-compose-master\wordpress-mysql\docker-compose.yaml') as file:
    data_yaml = yaml.full_load(file)
    services = data_yaml['services']

    print(services['db']['image'])
    for item, doc in data_yaml.items():
        print(item, ":", doc)



'''
for key in js.keys():
    print ("- ", key)
ss = js['test1']
ss['Add remote server ip'] = '0.0.0.0'
print(ss['Add remote server ip'])
'''

'''
os.path.join('.','files_json', 'menu_data.json')
path_folder = Path(os.path.join('.','files_json', 'menu_data.json')).parent.absolute()

print(path_folder)
'''


'''
#sourcepath = 'C:\\Users\\gta20\\AppData\\Local\\Temp\\tmpo2axqqcn\\docs'
dst = './t'
temp_dir = tempfile.mkdtemp()
print(temp_dir)
args = ['git', 'clone', '--depth=1', 'https://github.com/CircleCI-Public/api-preview-docs', temp_dir]
res = subprocess.Popen(args, stdout=subprocess.PIPE)
output, _error = res.communicate()

if not _error:
    #print(output)
    # Copy desired file from temporary dir
    #temp_dir = os.path.join(temp_dir, 'docs')
    files_yml = glob.glob1(temp_dir, '*.yml')
    files_env = glob.glob1(temp_dir, '*.env')
    for i in files_yml:
        print('Moving file >> ', i)
        shutil.move(os.path.join(temp_dir, i), os.path.join(dst, i))
    for k in files_env:
        print('Moving file >> ', k)
        shutil.move(os.path.join(temp_dir, k), os.path.join(dst, k))
    # Remove temporary dir
    shutil.rmtree(temp_dir)
else:
    print(_error)
'''
'''
# Create temporary dir
t = tempfile.mkdtemp()
# Clone into temporary dir
git.Repo.clone_from('stack@127.0.1.7:/home2/git/stack.git', t, branch='master', depth=1)
# Copy desired file from temporary dir
shutil.move(os.path.join(t, 'name.yaml'), '.')
# Remove temporary dir
shutil.rmtree(t)
'''
'''
dest = '/home/emilio1195/'
folder = 'folder_test/carpeta 2'
source = input('path: ')
install_name = 'docker_test'
cmd = "cd {name}; docker-compose -f {name}_docker-compose.yaml up".format(name=install_name)
print(cmd)
print(source + '\n')
print(source.replace('\\\\','\\'))
print(os.path.isdir(source))
source = os.path.expandvars(source).rstrip('\\').rstrip('/')
dest = os.path.expandvars(dest).rstrip('\\').rstrip('/')
txt = source.rsplit('\\', maxsplit=1)
print(txt)
print(dest.rsplit('/', maxsplit=1))
comando = 'vedraxx copy'
numer_spc = comando.count(' ')
print(comando.count(' '))
split_arr = comando.rsplit(' ', maxsplit=numer_spc-1)
print(split_arr)
print(split_arr[2:][0])
'''

'''
for root, dirs, files in os.walk(os.path.join(source,folder), topdown=True):
   for name in files:
      print("files> ")
      print(os.path.join(root, name))
      print("root> ", root)
      sub_path = ''.join(root.rsplit(source))[1:]
      print("rsplit> ", os.path.join(root, name), os.path.join(dest, sub_path, name))
   for name in dirs:
      print("Dir> ")
      print(os.path.join(root, name))
      print("rsplit> ", os.path.join(dest, ''.join(root.rsplit(source))[1:], name))
'''