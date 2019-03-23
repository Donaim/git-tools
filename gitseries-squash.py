#! /usr/bin/env python3

from common import *

import sys

args = sys.argv

if len(args) != 2:
	print('Expected single argument as top of squash', file=sys.stderr)
	exit(1)

squash_top = args[1]
squash_top_hash = get_commit_hash(squash_top)



