#!/usr/bin/env python

import commands
import raserver
import socket
import sys


def push():
    if len(sys.argv) < 4:
        print "%s push <url> <project> <branch>" % sys.argv[0]
        return
    url, project, branch = sys.argv[2:]
    # 1.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((url, raserver.PORT))
        sock.sendall(project + ':' + branch)

        # 4a.
        dest = "git://%s/%s" % (url, sock.recv(1024))

        # 4.
        print commands.getoutput("git remote set-url dest "+dest)
        print "pushing changes to", dest
        print commands.getoutput("git push dest "+branch)

        # 5a.
        sock.sendall("success")

        # 8.
        print sock.recv(1024)
    except:
        pass
    finally:
        sock.close()


ACTIONS = {
    'push': push,
}


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ACTIONS:
        ACTIONS[sys.argv[1]]()
    else:
        print sys.argv[0], "expects a command as its first argument"
