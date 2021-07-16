import pty, sys
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from os import fork, waitpid, execv, read, write
import dataV


class classSsh():
    def __init__(self, host=dataV.HOST, execute='echo "done" > /root/testing.txt', askpass=False, user=dataV.USER, password=b''.join(dataV.PASS)):
        self.exec = execute
        self.host = host
        self.user = user
        self.password = password
        self.askpass = askpass
        self.run()

    def run(self):
        command = [
                '/usr/bin/ssh',
                self.user+'@'+self.host,
                '-o', 'NumberOfPasswordPrompts=1',
                self.exec,
        ]

        # PID = 0 for child, and the PID of the child for the parent
        pid, child_fd = pty.fork()

        if not pid: # Child process
            # Replace child process with our SSH process
            execv(command[0], command)

        ## if we havn't setup pub-key authentication
        ## we can loop for a password promt and "insert" the password.
        while self.askpass:
            try:
                output = read(child_fd, 1024).strip()
            except:
                break
            lower = output.lower()
            # Write the password
            if b'password:' in lower:
                write(child_fd, self.password + b'\n')
                break
            elif b'are you sure you want to continue connecting' in lower:
                # Adding key to known_hosts
                write(child_fd, b'yes\n')
            elif b'company privacy warning' in lower:
                pass # This is an understood message
            else:
                print('Error:',output)

        waitpid(pid, 0)

shh = classSsh()