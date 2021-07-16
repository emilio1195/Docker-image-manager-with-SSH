import subprocess
import sys
import threading

# we'll be using a separate thread and a timed event to request the user input
import dataV


def timed_user_input(timer, wait, buffer_in, buffer_out, buffer_target):
    while True:  # user input loop
        timer.wait(wait)  # wait for the specified time...
        if not timer.is_set():  # if the timer was not stopped/restarted...
            print("Input: ", end="", file=buffer_out, flush=True)  # print the input prompt
            print(buffer_in.readline(), file=buffer_target, flush=True)  # forward the input
        timer.clear()  # reset the 'timer' event

if __name__ == "__main__":  # a guard from unintended usage
    input_buffer = sys.stdin  # a buffer to get the user input from
    output_buffer = sys.stdout  # a buffer to write rasa's output to
    conexSSH = "ssh " + dataV.USER + '@' + dataV.HOST
    cmd = input('cmd >> ')
    # for path in run(conexSSH + ' ' + cmd):
    # print(path)
    proc = subprocess.Popen(conexSSH + ' ' + cmd,  # start the process
                            stdin=subprocess.PIPE,  # pipe its STDIN so we can write to it
                            stdout=subprocess.PIPE,  # pipe its STDIN so we can process it
                            universal_newlines=True)
    # lets build a timer which will fire off if we don't reset it
    timer = threading.Event()  # a simple Event timer
    input_thread = threading.Thread(target=timed_user_input,
                                    args=(timer,  # pass the timer
                                          1.0,  # prompt after one second
                                          input_buffer, output_buffer, proc.stdin))
    input_thread.daemon = True  # no need to keep the input thread blocking...
    input_thread.start()  # start the timer thread
    # now we'll read the `rasa` STDOUT line by line, forward it to output_buffer and reset
    # the timer each time a new line is encountered
    for line in proc.stdout:
        output_buffer.write(line)  # forward the STDOUT line
        output_buffer.flush()  # flush the output buffer
        timer.set()  # reset the timer