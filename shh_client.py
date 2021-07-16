import select
import time
from filecmp import cmp

import paramiko
import dataV

#command for remove all content into main folder --> rm -rf *

class Conex_ssh:
    def __init__(self):
        print("Conecting Server Remote...")
        try:
            self.client_ssh = paramiko.SSHClient()
            self.client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # password = input('Pass: ')
            self.client_ssh.connect(hostname=dataV.HOST, username=dataV.USER, password=dataV.PASS)
            print("Conection Ok!")
            self.set_status_conx(True)
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

    def set_status_conx(self, e):
        self.e = e
    def get_status_conx(self):
        return self.e

    def open_sftp(self):
        try:
            self.sftp = self.client_ssh.open_sftp()
            return self.sftp
        except:
            print("Open sftp Fail!\nCheck your connection Internet or credentials by server remote")
            return None

    def command_client(self, command):
        list_line = []
        std_input, std_output, std_error = self.client_ssh.exec_command(command, get_pty=True)
        output = std_output.readlines()
        timeout = 30

        if std_output.channel.recv_exit_status() == 0:
            print("Command Ok!")
            endtime = time.time() + timeout

            for line in output:
                line = line.replace('\n', '')
                print(' ###> ', line)
                list_line.append(line)
            time.sleep(1)  # Recommend sleep thread for secure in the conection

            if std_output.channel.eof_received:
                std_output.channel.close()

            return list_line

        else:
            print("Command Fail!")
            return []



    def client_ssh_close(self):
        self.client_ssh.close()

    def sftp_close(self):
        self.sftp.close()
