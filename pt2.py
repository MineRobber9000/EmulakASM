import parse

instr = parse.InstructionList("instructions.txt")

op = "jp $6000"

id = parse.parse_opcode_num(instr,op)

bytes = parse.parse_opcode(instr,id,op)

print " ".join(hex(x)[2:].zfill(2) for x in bytes)
#print bytes
