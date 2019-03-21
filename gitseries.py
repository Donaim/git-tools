#! /usr/bin/env python3

DEVEL_ENDING = '-devel'

import subprocess
import sys
import os

CURENT_DIR = os.path.dirname(__file__)

def exre(cmd: str) -> str:
	print('\n> {}'.format(cmd))
	result = subprocess.check_output(cmd, shell=True)
	result = result.decode('utf-8')
	return result.strip()

def exout(cmd: str):
	print('\n> {}'.format(cmd))
	return subprocess.check_call(cmd, shell=True)

def get_empty_commits(last_commit: str) -> list:
	def get_parsed_log() -> iter:
		range = ('"{}~1"..HEAD'.format(last_commit)) if last_commit else ''
		raw = exre("git log --format='%H %T' {}".format(range))
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
	return exre('git rev-parse --abbrev-ref HEAD')

def branch_exists_q(name: str) -> bool:
	try:
		branches = exre('git branch')
		return any([b.strip() == name for b in branches.split('\n')])
	except:
		return False

def get_common_ancestor(branch1: str, branch2: str) -> str:
	return exre('git merge-base "{}" "{}"'.format(branch1, branch2))

def get_branch_hash(name: str) -> str:
	return exre('git rev-parse "{}"'.format(name))

def gassert(b: bool, message: str) -> None:
	if not b:
		print('{}'.format(message), file=sys.stderr)
		exit(1)

# print('curent branch: ' + get_current_branch().strip())
# print(get_parsed_log())

current_branch = get_current_branch()
gassert(current_branch.endswith(DEVEL_ENDING), 'should end with -devel')

main_branch = current_branch[:-len(DEVEL_ENDING)]
gassert(len(main_branch) > 0, 'invalid current branch name')

# print('main branch = "{}"'.format(main_branch))
# print('exists: ' + str(branch_exists_q('master')))

common_ancestor = None

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
	exout('git branch -D "{}"'.format(main_branch))

exout('git checkout -b "{}"'.format(main_branch))

if not empty_commits:
	print("DONE: no empty commits")
	exit(0)

rebase_point = empty_commits[0]
ignored_array = ' '.join(empty_commits)
editor_path = os.path.join(CURENT_DIR, 'fix-all-except.py')
cmd = 'GIT_SEQUENCE_EDITOR="{} {}" git rebase --interactive --keep-empty "{}~1"'.format(editor_path, ignored_array, rebase_point)
exout(cmd)
