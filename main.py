#! /usr/bin/env python3


import subprocess
import sys

DEVEL_ENDING = '-devel'

def ex(cmd: str) -> str:
	print('ex: {}'.format(cmd))

	result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
	result = result.decode('utf-8')
	return result

def ex_out(cmd: str):
	print('ex: {}'.format(cmd))

	return subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)

def exgit(s: str) -> str:
	return ex('git ' + s)


def get_empty_commits(last_commit: str) -> list:
	def get_parsed_log() -> iter:
		raw = exgit("log --format='%H %T' '{}~1'..HEAD".format(last_commit)).strip()
		lines = raw.split('\n')
		for line in lines:
			yield line.split()

	def get_iters():
		prev = None
		for p in reversed(list(get_parsed_log())):
			(H, T) = p
			if T == prev:
				yield H
			else:
				prev = T

	return list(get_iters())

def get_current_branch() -> str:
	return exgit('rev-parse --abbrev-ref HEAD').strip()

def branch_exists_q(name: str) -> bool:
	try:
		branches = exgit('branch')
		return any([b.strip() == name for b in branches.split('\n')])
	except:
		return False

def get_save_tag(branch_name: str) -> str:
	''' For saving before doing reset --hard '''

	alltags = exgit('tag --list').strip().split('\n')

	prefix = 'gitseries-save@' + branch_name + '@'
	prefixlen = len(prefix)
	savetags = list(filter(lambda x: x.startswith(prefix), alltags))

	if not savetags:
		return prefix + '0'

	numbers = [t[prefixlen:] for t in savetags]
	last = list(sorted(numbers))[-1]
	lasti = int(last)

	return prefix + str(lasti + 1)

def get_common_ancestor(branch1: str, branch2: str) -> str:
	return exgit('merge-base "{}" "{}"'.format(branch1, branch2)).strip()

def get_branch_hash(name: str) -> str:
	return exgit('rev-parse "{}"'.format(name)).strip()

def gassert(b: bool, message: str) -> None:
	if not b:
		print('{}'.format(message), file=sys.stderr)
		exit(1)

print('hello')

# print('curent branch: ' + get_current_branch().strip())
# print(get_parsed_log())

current_branch = get_current_branch()
gassert(current_branch.endswith(DEVEL_ENDING), 'should end with -devel')

main_branch = current_branch[:-len(DEVEL_ENDING)]
gassert(len(main_branch) > 0, 'invalid current branch name')

# print('main branch = "{}"'.format(main_branch))
# print('exists: ' + str(branch_exists_q('master')))

common_ancestor = None

# save_tag = get_save_tag(main_branch)
# ex_out('git tag "{}"'.format(save_tag))
# print('savetag = {}'.format(save_tag))

if branch_exists_q(main_branch):
	print('"{}" exists'.format(main_branch))
	common_ancestor = get_common_ancestor(main_branch, current_branch)
else:
	print('"{}" does not exist'.format(main_branch))
	common_ancestor = None

print('common ancestor: {}'.format(common_ancestor))

empty_commits = get_empty_commits(common_ancestor)
# print('empty commits: \n\t{}'.format('\n\t'.join(empty_commits)))

if common_ancestor:
	exgit('branch -D "{}"'.format(main_branch))

exgit('checkout -b "{}"'.format(main_branch))

if not empty_commits:
	print("DONE: no empty commits")
	exit(0)

rebase_point = empty_commits[0]
ignored_array = ' '.join(empty_commits)
cmd = 'GIT_SEQUENCE_EDITOR="fix-all-except.py {}" git rebase --interactive --keep-empty "{}~1"'.format(ignored_array, rebase_point)
print('cmd: {}'.format(cmd))
subprocess.check_call(cmd, shell=True)
