opcode_start = 0
opcodes_implemented = 0x1e
for i in range(opcode_start,opcodes_implemented):
	print "print_op(\"\",0x{})".format(hex(i)[2:].zfill(2))
