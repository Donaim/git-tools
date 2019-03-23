
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

def get_commit_hash(commit_abbrev: str) -> str:
	return exre('git rev-parse "{}"'.format(commit_abbrev))

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