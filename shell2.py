import os
import tempfile
import time
from subprocess import Popen, PIPE

import pexpect

import dataV


def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    process.wait()
    cont = 0
    while True:
        line = process.stdout.readline().rstrip()
        time.sleep(1)
        if not line:
            cont += 1
            if cont == 5:
                break
        yield line



if __name__ == "__main__":
    conexSSH = "ssh " + dataV.USER + '@' + dataV.HOST
    cmd = input('cmd >> ')
    #for path in run(conexSSH + ' ' + cmd):
        #print(path)
