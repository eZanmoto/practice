#!/usr/bin/env python

import os
import sys
import vcs


def init():
    if len(sys.argv) < 4:
        print "%s init <type> <name>" % sys.argv[0]
        return
    repo_type = sys.argv[2].lower()
    repo_name = sys.argv[3]
    if repo_type in vcs.impls.keys():
        try:
            os.mkdir(repo_name)
        except OSError:
            print "'%s' already exists in this directory" % repo_name
            return
        os.chdir(repo_name)
        vcs.impls[repo_type].init()
        print "Initialized empty", repo_type, "repository in", os.path.abspath(repo_name)
    else:
        print "Unknown repo type"


ACTIONS = {
    'init': init,
}


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ACTIONS:
        ACTIONS[sys.argv[1]]()
    else:
        print sys.argv[0], "expects a command as its first argument"
