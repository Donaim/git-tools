#! /usr/bin/env python3

from common import *
import gitseries

cs = gitseries.CurrentSeries()

commits = list(reversed(cs.empty_commits))

print('')
print('Series:')
for (i, c) in enumerate(commits):
	print('\t{}) {}'.format(i, c.s))
print('\t{}) {}'.format(len(commits), "BASE"))

index  = int(input('Chosen: '))
if index == 0:
	exit(0)

# Get last commit of that patch series
next   = commits[index - 1].H
edit   = get_commit_hash('{}~1'.format(next))

run_editor(['--edit', edit], edit)
