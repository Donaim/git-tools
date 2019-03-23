#! /usr/bin/env python3

from common import *
import gitseries

import sys

args = sys.argv

if len(args) != 2:
	print('Expected single argument as top of squash', file=sys.stderr)
	exit(1)

squash_top = args[1]
squash_top_hash = get_commit_hash(squash_top)

(ignored_array, rebase_point, _, _) = gitseries.get_editor_params()
print('rebase point: {}'.format(rebase_point))
commits = get_commits(rebase_point)

print('commits:\n\t{}'.format('\n\t'.join(commits)))

