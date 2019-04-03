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

cs = gitseries.CurrentSeries()

commits = get_commits(cs.rebase_point)
take = list(takewhile( lambda c: c.H != squash_top_hash, commits ))
print('taken: \n\t{}'.format('\n\t'.join(str(c) for c in take)))

savetag = get_save_tag(cs.current_branch)
exout('git tag "{}"'.format(savetag))

non_empty = [c for c in cs.commits if c not in cs.empty_commits]
hashes = [c.H for c in non_empty + take]
run_editor(['--fixup'] + hashes, cs.rebase_point)

