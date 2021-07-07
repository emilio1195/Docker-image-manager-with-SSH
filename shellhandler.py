import select
import time
import paramiko

import data


class ShellHandler:
    def __init__(self, host, user, psw):
        print("Initialising instance of ShellHandler host:{0}".format(host))
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(host, username=user, password=psw, port=22)
            self.channel = self.ssh.invoke_shell()
        except:
            print("Error Creating ssh connection to {0}".format(host))
            print("Exiting ShellHandler")
            return
        self.psw = psw
        self.stdin = self.channel.makefile('wb')
        self.stdout = self.channel.makefile('r')
        self.host = host
        time.sleep(2)

        while not self.channel.recv_ready():
            time.sleep(2)
        self.initialprompt = ""
        while self.channel.recv_ready():

            rl, wl, xl = select.select([self.stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                tmp = self.stdout.channel.recv(1024)
                self.initialprompt = self.initialprompt + str(tmp.decode())

    def __del__(self):
        self.ssh.close()
        print("closed connection to {0}".format(self.host))

    def execute(self, cmd):
        cmd = cmd.strip('\n')
        print("Waiting...")
        self.stdin.write(cmd + '\n')
        # self.stdin.write(self.psw +'\n')
        self.stdin.flush()
        time.sleep(1)
        while not self.stdout.channel.recv_ready():
            time.sleep(2)
            print("Waiting for recv_ready")

        output = ""

        while self.channel.recv_ready():
            rl, wl, xl = select.select([self.stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                #cont = 0
                tmp = self.stdout.channel.recv(1024)
                output = str(tmp.decode("utf-8")).strip('\r\n')
                array = output.replace('\r', '').split('\n')
                for line in array:
                    if not ' ... ' in line:
                        if "" != line:
                            print(line)
                    else:
                        for subline in line.split(' ... '):
                            if "" != subline:
                                print(subline)
                array.clear()

            if '$' in output:
                print("\nFinish.\n")
                break
            if 'command not found' in output:
                print("\nFinish.\n")
                break
            '''
            if cont > 3:
                if temp_out in output:
                    print("\nFinish.\n")
                    break
            '''

            if 'password' in output:
                self.stdin.write(input('pass: ')+'\n') #It is important sum the char \n
                output = ''

            elif '[Y/n] ' in output:
                self.stdin.write(input('[Y/n]: ')+'\n')
                output = ''

            time.sleep(1)

        return output

    def client_ssh_close(self):
        self.ssh.close()

    def open_sftp(self):
        try:
            self.sftp = self.client_ssh.open_sftp()
            return self.sftp
        except:
            print("Open sftp Fail!\nCheck your connection Internet or credentials by server remote")
            return None

    def sftp_close(self):
        self.ssh.close()

ssh = ShellHandler(data.HOST, data.USER, data.PASS)
while True:
    cmd = input("cmd >> ")
    ssh.execute(cmd)