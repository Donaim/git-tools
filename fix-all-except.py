#! /usr/bin/env python3

import sys


args = sys.argv[1:]

file    = args[-1]
exclude = args[:-1]

def line_get_hash(line: str) -> str:
	return line.split()[1]

def line_is_useful(line: str) -> bool:
	return line.strip() and not line[0] == '#'

def get_correct_line(line: str, excluded: bool) -> str:
	if excluded:
		return line
	else:
		(cmd, space, rest) = line.partition(' ')
		return 'fixup' + space + rest

lines = None
with open(file, 'r') as r:
	lines = r.readlines()

lines = list(filter(line_is_useful, lines))

mapped = [(line, line_get_hash(line)) for line in lines]

with open(file, 'w') as w:
	for m in mapped:
		(line, hash) = m
		excluded = any(ex.startswith(hash) for ex in exclude)
		modified = get_correct_line(line, excluded)
		print('\t' + modified, end='')
		w.write(modified)
