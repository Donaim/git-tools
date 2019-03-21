
import subprocess


def ex(cmd: str) -> str:
	print('ex: {}'.format(cmd))

	result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
	result = result.decode('utf-8')
	return result

def exgit(s: str) -> str:
	return ex('git ' + s)



