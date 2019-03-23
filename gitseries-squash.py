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

(picked, rebase_point, _, _, current_branch) = gitseries.get_editor_params()

savetag = get_save_tag(current_branch)
exout('git tag "{}"'.format(savetag))

commits = get_commits(rebase_point)
take = list(takewhile( lambda c: c.H != squash_top_hash, commits ))
print('taken: \n\t{}'.format('\n\t'.join(str(c) for c in take)))

picked += take
run_editor(picked, rebase_point)
