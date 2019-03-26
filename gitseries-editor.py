#! /usr/bin/env python3

import sys


args = sys.argv[1:]

file = args[-1]

di = {}
curr = None
for a in args[:-1]:
	if a.startswith("--"):
		curr = a[2:]
	else:
		di[a]     = curr
		di[a[:7]] = curr
		di[a[:8]] = curr
		di[a[:9]] = curr

def line_get_hash(line: str) -> str:
	return line.split()[1]

def line_is_useful(line: str) -> bool:
	return line.strip() and not line[0] == '#'

lines = None
with open(file, 'r') as r:
	lines = r.readlines()

with open(file, 'w') as w:
	for line in lines:
		if line_is_useful(line):
			(pcmd, space, rest) = line.partition(' ')
			(hash, space, desc) = rest.partition(' ')

			correct = line
			if hash in di:
				pcmd = di[hash]
				correct = pcmd + space + rest

			print('\t' + pcmd + space + desc, end='')
			w.write(correct)
