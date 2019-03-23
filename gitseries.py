#! /usr/bin/env python3

DEVEL_ENDING = '-devel'

from common import *

current_branch = get_current_branch()
print('curent branch: ' + current_branch)
gassert(current_branch.endswith(DEVEL_ENDING), 'should end with -devel')

main_branch = current_branch[:-len(DEVEL_ENDING)]
gassert(len(main_branch) > 0, 'invalid current branch name')

if branch_exists_q(main_branch):
	print('"{}" exists'.format(main_branch))
else:
	print('"{}" does not exist'.format(main_branch))

common_ancestor = get_common_ancestor(main_branch, current_branch)
print('common ancestor: {}'.format(common_ancestor))

empty_commits = get_empty_commits(common_ancestor)
print('empty commits: \n\t{}'.format('\n\t'.join(empty_commits)))

if common_ancestor:
	exout('git branch -D "{}"'.format(main_branch))

exout('git checkout -b "{}"'.format(main_branch))

rebase_point = empty_commits[0]
ignored_array = ' '.join(empty_commits)
cmd = 'GIT_SEQUENCE_EDITOR="{} {}" git rebase --interactive --keep-empty "{}~1"'.format('gitseries-editor.py', ignored_array, rebase_point)
exout(cmd)
