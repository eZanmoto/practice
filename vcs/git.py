import commands
import os.path
import socket

import raserver


def init():
    commands.getoutput("git init --bare")


def detect():
    return os.path.isdir('.git')


def push(project, branch, url):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((url, raserver.PORT))
        sock.sendall(project + '\n' + branch + '\n')
        dir = sock.recv(1024)
        print dir
        if dir.startswith("error"):
            return
    except:
        return
    finally:
        sock.close()
    dest = "git://"+url+"/"+dir
    print dest
    print commands.getoutput("git remote set-url dest "+dest)
    print commands.getoutput("git push dest "+branch)
