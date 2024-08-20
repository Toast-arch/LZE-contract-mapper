import sys

from .lzecm import LZECM
from .parser import ArgParser

def main(sys_args):
	parser = ArgParser()
	
	parser.prog = "lze-contract-mapper"
	
	args = None

	try:
		args = parser.parse_args(sys_args)
	except ValueError:
		return 1

	lzecm_main = LZECM()

	lzecm_main.run()

	return 0

def run():
	return main(sys.argv[1:])

if __name__ == "__main__":
	run()