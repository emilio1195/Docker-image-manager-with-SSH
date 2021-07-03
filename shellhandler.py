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
                tmp = self.stdout.channel.recv(1024)
                output = output + str(tmp.decode("utf-8"))
        print(output)
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