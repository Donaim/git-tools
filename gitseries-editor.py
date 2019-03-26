#! /usr/bin/env python3

import sys


args = sys.argv[1:]

file = args[-1]

di = {}
curr = None
for a in args[1:-1]:
	if a.startswith("--"):
		curr = a[2:]
		di[curr] = []
	else:
		di[curr].append(a)

def line_get_hash(line: str) -> str:
	return line.split()[1]

def line_is_useful(line: str) -> bool:
	return line.strip() and not line[0] == '#'

def get_correct_line(line: str, hash: str) -> str:
	for k in di:
		if any(c.startswith(hash) for c in di[k]):
			(_, space, rest) = line.partition(' ')
			return k + space + rest
	return line

lines = None
with open(file, 'r') as r:
	lines = r.readlines()

lines = list(filter(line_is_useful, lines))

mapped = [(line, line_get_hash(line)) for line in lines]

with open(file, 'w') as w:
	for (line, hash) in mapped:
		modified = get_correct_line(line, hash)
		print('\t' + modified, end='')
		w.write(modified)
