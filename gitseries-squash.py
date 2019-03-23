#! /usr/bin/env python3

from common import *
import gitseries

import sys
from itertools import *

args = sys.argv

if len(args) != 2:
	print('Expected single argument as top of squash', file=sys.stderr)
	exit(1)

squash_top = args[1]
squash_top_hash = get_commit_hash(squash_top)
print('squash top hash: {}'.format(squash_top_hash))

(ignored_array, rebase_point, _, _) = gitseries.get_editor_params()

try: exout("git branch -D tmp")
except: pass
exout("git checkout -b tmp")

commits = get_commits(rebase_point)
cs = [str(c) for c in commits]
print('commits:\n\t{}'.format('\n\t'.join(cs)))

# dropwhile()
