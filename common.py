
import subprocess
import sys
import os

DEVEL_ENDING = '-devel'

def exre(cmd: str) -> str:
	print('\n> {}'.format(cmd))
	result = subprocess.check_output(cmd, shell=True)
	result = result.decode('utf-8')
	return result.strip()

def exout(cmd: str):
	print('\n> {}'.format(cmd))
	return subprocess.check_call(cmd, shell=True)

class Commit:
	def __init__(self, H, T, s):
		self.H = H
		self.T = T
		self.s = s
	
	def __str__(self) -> str:
		return "{} {}".format(self.H[:7], self.s)

def get_commits(last_commit: str) -> list:
	def iterator():
		range = ('"{}~1"..HEAD'.format(last_commit)) if last_commit else ''
		raw = exre("git log --format='%H %T %s' {}".format(range))
		lines = raw.split('\n')
		for line in lines:
			sp = line.split()
			H = sp[0]
			T = sp[1]
			s = line[len(H) + 1 + len(T) + 1:]
			yield Commit(H, T, s)
	return list(iterator())

def get_empty_commits(last_commit: str) -> list:
	def get_iters():
		prev = None
		for p in reversed(get_commits(last_commit)):
			if p.T == prev:
				yield p
			else:
				prev = p.T

	return list(get_iters())

def get_commit_hash(commit_abbrev: str) -> str:
	return exre('git rev-parse "{}"'.format(commit_abbrev))

def get_commit_print(commit_hash: str) -> str:
	ret = subprocess.check_output('git show --quiet --format="%h %s" "{}"'.format(commit_hash), shell=True)
	return ret.decode('utf-8').strip()

def get_current_branch() -> str:
	return exre('git rev-parse --abbrev-ref HEAD')

def branch_exists_q(name: str) -> bool:
	branches = exre('git branch')
	return any(b.strip('*').strip() == name for b in branches.split('\n'))

def get_common_ancestor(branch1: str, branch2: str) -> str:
	try:
		re = exre('git merge-base "{}" "{}"'.format(branch1, branch2))
		if re:
			return re
		else:
			return None
	except:
		return None

def get_branch_hash(name: str) -> str:
	return exre('git rev-parse "{}"'.format(name))

def gassert(b: bool, message: str) -> None:
	if not b:
		print('{}'.format(message), file=sys.stderr)
		exit(1)

def run_editor(ignored_array: list, rebase_point: str):
	cmd = 'GIT_SEQUENCE_EDITOR="{} {}" git rebase --interactive --keep-empty "{}~1"'.format('gitseries-editor.py', ignored_array, rebase_point)
	exout(cmd)
