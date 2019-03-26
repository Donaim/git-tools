#! /usr/bin/env python3

from common import *

class CurrentSeries:
	def __init__(self):
		self.current_branch = get_current_branch()
		print('curent branch: ' + self.current_branch)
		gassert(self.current_branch.endswith(DEVEL_ENDING), 'should end with -devel')

		self.main_branch = self.current_branch[:-len(DEVEL_ENDING)]
		gassert(len(self.main_branch) > 0, 'invalid current branch name')

		if branch_exists_q(self.main_branch):
			print('"{}" exists'.format(self.main_branch))
		else:
			print('"{}" does not exist'.format(self.main_branch))

		self.common_ancestor = get_common_ancestor(self.main_branch, self.current_branch)
		print('common ancestor: {}'.format(get_commit_print(self.common_ancestor)))

		self.empty_commits = get_empty_commits(self.common_ancestor)
		print('empty commits: \n\t{}'.format('\n\t'.join(str(c) for c in self.empty_commits)))
		self.rebase_commit = self.empty_commits[0]
		self.rebase_point = self.rebase_commit.H
		print('rebase point:\n\t{}'.format(str(self.rebase_commit)))

if __name__ == '__main__':
	cs = CurrentSeries()

	if cs.common_ancestor:
		exout('git branch -D "{}"'.format(cs.main_branch))

	exout('git checkout -b "{}"'.format(cs.main_branch))

	run_editor(cs.empty_commits, cs.rebase_point)

