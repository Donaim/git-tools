
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

def exoutn(cmd: str):
	print('> {}'.format(cmd))
	return subprocess.check_call(cmd, shell=True)

class Commit:
	def __init__(self, H, T, s):
		self.H = H
		self.T = T
		self.s = s
	
	def __str__(self) -> str:
		return "{} {}".format(self.H[:7], self.s)

COMMIT_FORMAT = '%H %T %s'

def get_commit_by_format(formatted: str) -> Commit:
	sp = formatted.split()
	H = sp[0]
	T = sp[1]
	s = formatted[len(H) + 1 + len(T) + 1:]
	return Commit(H, T, s)

def get_commit_by_hash(commit_abbrev: str) -> Commit:
	formatted = exre("git show --quiet --format='{}' '{}'".format(COMMIT_FORMAT, commit_abbrev))
	return get_commit_by_format(formatted)

def get_commits(last_commit: str) -> list:
	range = ('"{}~1"..HEAD'.format(last_commit)) if last_commit else ''
	raw = exre("git log --format='{}' {}".format(COMMIT_FORMAT, range))
	lines = raw.split('\n')
	return list(map(get_commit_by_format, lines))

def get_empty_commits(all_commits: list) -> list:
	def get_iters():
		prev = None
		for p in reversed(all_commits):
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

def check_tag_exists(name: str) -> bool:
	alltags = exre('git tag --list').split('\n')
	return bool(name in alltags)

def get_save_tag(branch_name: str, new: bool = False) -> str:
	''' For saving before doing reset --hard or rebase '''

	alltags = exre('git tag --list').split('\n')

	prefix = 'gitseries-save@' + branch_name + '@'
	prefixlen = len(prefix)
	savetags = list(filter(lambda x: x.startswith(prefix), alltags))

	if not savetags:
		return prefix + '0'

	numbers = [t[prefixlen:] for t in savetags]
	last = list(sorted(numbers))[-1]

	if new:
		lasti = int(last)
		return prefix + str(lasti + 1)
	else:
		return last

def gassert(b: bool, message: str) -> None:
	if not b:
		print('{}'.format(message), file=sys.stderr)
		exit(1)

def run_editor(args: list, rebase_point: str):
	args = ' '.join(args)
	cmd = 'GIT_SEQUENCE_EDITOR="{} {}" git rebase --interactive --keep-empty "{}~1"'.format('gitseries-editor.py', args, rebase_point)
	exout(cmd)
