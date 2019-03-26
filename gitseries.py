#! /usr/bin/env python3

from common import *

SERIES_BEGIN_TAG_PREFIX = 'gitseries-begin@'

class CurrentSeries:
	def __init__(self):
		self.current_branch = get_current_branch()
		print('curent branch: ' + self.current_branch)
		gassert(self.current_branch.endswith(DEVEL_ENDING), 'should end with -devel')

		self.main_branch = self.current_branch[:-len(DEVEL_ENDING)]
		gassert(len(self.main_branch) > 0, 'invalid current branch name')

		if branch_exists_q(self.main_branch):
			print('"{}" exists'.format(self.main_branch))
			self.common_ancestor = get_common_ancestor(self.main_branch, self.current_branch)
		else:
			print('"{}" does not exist'.format(self.main_branch))
			last = None
			last_tag = SERIES_BEGIN_TAG_PREFIX + self.main_branch
			if check_tag_exists(last_tag):
				last = last_tag
				print('using {} as common ancestor'.format(last_tag))
			else:
				print('tag {} does not exists -> using --root as common ancestor'.format(last_tag))
			self.common_ancestor = last

		print('common ancestor: {}'.format(get_commit_print(self.common_ancestor)))

		self.commits = get_commits(self.common_ancestor)
		self.empty_commits = get_empty_commits(self.commits)
		print('empty commits: \n\t{}'.format('\n\t'.join(str(c) for c in self.empty_commits)))
		self.rebase_commit = self.empty_commits[0]
		self.rebase_point = self.rebase_commit.H
		print('rebase point:\n\t{}'.format(str(self.rebase_commit)))

if __name__ == '__main__':
	cs = CurrentSeries()

	try: exout('git branch -D "{}"'.format(cs.main_branch))
	except: pass
	exout('git checkout -b "{}"'.format(cs.main_branch))

	not_empty = [c for c in cs.commits if c not in cs.empty_commits]
	not_empty_hashes = [c.H for c in not_empty]
	run_editor(['--fixup'] + not_empty_hashes, cs.rebase_point)

