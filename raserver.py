#!/usr/bin/env python

import commands
import os
import SocketServer
import subprocess
import tempfile


tmpdir_path = tempfile.mkdtemp()


PORT = 9428


class ChangeDirectory:
    def __init__(self, new_dir):
        self._new_dir = new_dir

    def __enter__(self):
        self._old_dir = os.getcwd()
        os.chdir(self._new_dir)
        return self._new_dir

    def __exit__(self, type, value, traceback):
        os.chdir(self._old_dir)
        return True


def chdir(new_dir):
    return ChangeDirectory(new_dir)


class RepoArmourServer(SocketServer.BaseRequestHandler):
    def handle(self):
        global tmpdir_path
        print "Handling request"
        # 1.
        project, branch = self.request.recv(1024).strip().split(':')

        try:
            self.update(project, branch)
            output = "success"
        except Exception as ex:
            output = "error: " + str(ex)
        self.request.sendall(output)

    def update(self, project, branch):
        # with open('remotes') as remotes:
        remotes = {
            'bake': ('https://github.com/eZanmoto/', 'Bake')
        }

        # 2.
        with chdir(tempfile.mkdtemp(dir=tmpdir_path)) as cwd:
            # 3.
            print commands.getoutput("git clone --bare %s/%s.git" % remotes[project])

            # 4.
            location = os.path.join(cwd, remotes[project][1]+'.git')
            self.request.sendall(os.path.relpath(location, tmpdir_path))

            # 5a.
            self.request.recv(1024)

            # 5.
            print commands.getoutput("git clone %s.git" % remotes[project][1])

            # 6.
            with chdir(remotes[project][1]):
                print commands.getoutput("ls")
            commands.getoutput("rm -rf %s" % remotes[project][1])

            # 7.
            with chdir(remotes[project][1]+'.git'):
                print commands.getoutput("git push -u origin master")
            commands.getoutput("rm -rf %s.git" % remotes[project][1])


if __name__ == '__main__':
    print "Starting Git daemon in ", tmpdir_path
    subprocess.Popen(("git daemon --reuseaddr --export-all --enable=receive-pack --base-path=%s %s" %
            (tmpdir_path, tmpdir_path)).split(' '))
    print "Running..."
    SocketServer.TCPServer(('localhost', PORT), RepoArmourServer).serve_forever()
