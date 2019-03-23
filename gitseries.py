#! /usr/bin/env python3

from common import *

def get_editor_params():
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
	print('common ancestor: {}'.format(get_commit_print(common_ancestor)))

	empty_commits = get_empty_commits(common_ancestor)
	print('empty commits: \n\t{}'.format('\n\t'.join(str(c) for c in empty_commits)))
	rebase_commit = empty_commits[0]
	rebase_point = rebase_commit.H
	print('rebase point:\n\t{}'.format(str(rebase_commit)))

	ignored_array = ' '.join(c.H for c in empty_commits)
	return (ignored_array, rebase_point, common_ancestor, main_branch)

if __name__ == '__main__':
	(ignored_array, rebase_point, common_ancestor, main_branch) = get_editor_params()

	if common_ancestor:
		exout('git branch -D "{}"'.format(main_branch))

	exout('git checkout -b "{}"'.format(main_branch))

	run_editor(ignored_array, rebase_point)
