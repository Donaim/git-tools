#! /usr/bin/env python3

from common import *

SERIES_BEGIN_TAG_PREFIX = 'gitseries-begin@'

class CurrentSeries:
	def __init__(self, create: bool = False):
		self.current_branch = get_current_branch()
		print('curent branch: ' + self.current_branch)
		gassert(self.current_branch.endswith(DEVEL_ENDING), 'should end with -devel')

		self.main_branch = self.current_branch[:-len(DEVEL_ENDING)]
		gassert(len(self.main_branch) > 0, 'invalid current branch name')

		if branch_exists_q(self.main_branch):
			print('"{}" exists'.format(self.main_branch))
		else:
			print('"{}" does not exist'.format(self.main_branch))
			if create: self.create_main_branch()
			else: return

		self.common_ancestor = get_common_ancestor(self.main_branch, self.current_branch)
		print('common ancestor: {}'.format(get_commit_print(self.common_ancestor)))

		self.commits = get_commits(self.common_ancestor)
		self.empty_commits = get_empty_commits(self.commits)
		print('empty commits: \n\t{}'.format('\n\t'.join(str(c) for c in self.empty_commits)))
		self.rebase_commit = self.empty_commits[0]
		self.rebase_point = self.rebase_commit.H
		print('rebase point:\n\t{}'.format(str(self.rebase_commit)))

	def create_main_branch(self):
		last = None
		last_tag = SERIES_BEGIN_TAG_PREFIX + self.main_branch
		if check_tag_exists(last_tag):
			last = last_tag
			print('using {} as rebase point'.format(last_tag))
		else:
			print('tag {} does not exists -> using --root as rebase point'.format(last_tag))

		all_commits = get_commits(last)
		empty_ones = get_empty_commits(all_commits)
		print('empty commits: \n\t{}'.format('\n\t'.join(str(c) for c in empty_ones)))

		first_empty = empty_ones[0]
		exout('git checkout "{}"~1 --quiet'.format(first_empty.H))
		exoutn('git branch "{}"'.format(self.main_branch))
		exoutn('git checkout "{}" --quiet'.format(self.current_branch))
		print("Created main branch")

if __name__ == '__main__':
	cs = CurrentSeries(True)

	exout('git branch -D "{}"'.format(cs.main_branch))
	exout('git checkout -b "{}"'.format(cs.main_branch))

	not_empty = [c for c in cs.commits if c not in cs.empty_commits]
	not_empty_hashes = [c.H for c in not_empty]
	run_editor(['--fixup'] + not_empty_hashes, cs.rebase_point)

