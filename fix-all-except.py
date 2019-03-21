#! /usr/bin/env python3

import sys


args = sys.argv[1:]

file    = args[-1]
exclude = args[:-1]

print('file = "{}" exclude = {}'.format(file, exclude))

