import sys
import os.path

version_fname = 'VERSION'

if not os.path.isfile(version_fname):
    sys.exit(1)

with open(version_fname) as f:
