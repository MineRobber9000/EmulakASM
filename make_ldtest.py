from __future__ import print_function
import sys

#print sys.argv
if len(sys.argv)>2:
	print("ld {},{}".format(*sys.argv[1:]),end="")
