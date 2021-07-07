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
            print("Conection Ok!")
            self.set_status_conx(True)
            self.channel = self.ssh.invoke_shell()
        except paramiko.AuthenticationException as authenticationException:
            print("Authentication failed, please verify your credentials: %s" % authenticationException)
            self.set_status_conx(False)
        except paramiko.SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            self.set_status_conx(False)
        except paramiko.BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            self.set_status_conx(False)
        except Exception as e:
            print(e.args)
            self.set_status_conx(False)

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

            if '$' == (array[-1]).rstrip(' '):
                print("\nFinish.\n")
                return '$'
            if 'command not found' in output:
                print("\nFinish.\n")
                return '$'
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

    def command_client(self, command):
        list_line = []
        std_input, std_output, std_error = self.ssh.exec_command(command, get_pty=True)
        output = std_output.readlines()
        timeout = 30

        if std_output.channel.recv_exit_status() == 0:
            print("Command Ok!")
            endtime = time.time() + timeout

            for line in output:
                line = line.replace('\n', '')
                print('>> ', line)
                list_line.append(line)
            time.sleep(1)  # Recommend sleep thread for secure in the conection

            if std_output.channel.eof_received:
                std_output.channel.close()

            return list_line

        else:
            print("Command Fail!")
            return []

    def set_status_conx(self, e):
        self.e = e

    def get_status_conx(self):
        return self.e

    def open_sftp(self):
        try:
            self.sftp = self.ssh.open_sftp()
            return self.sftp
        except:
            print("Open sftp Fail!\nCheck your connection Internet or credentials by server remote")
            return None

    def client_ssh_close(self):
        self.ssh.close()

    def sftp_close(self):
        self.sftp.close()