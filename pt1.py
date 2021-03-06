import parse

instr = parse.InstructionList("instructions.txt")

def print_op(o,eop):
	op = parse.parse_opcode_num(instr,o)
	assert op==eop, "Opcode {} failed to parse correctly".format(o)
	print "\"{}\": ${}".format(o,hex(op)[2:].zfill(2).upper())

print_op("nop",0x00)
print_op("jp $6000",0x01)
print_op("call $7000",0x02)
print_op("ret",0x03)
print_op("ld a,$ff",0x04)
print_op("ld b,$ff",0x05)
print_op("ld c,$ff",0x06)
print_op("ld d,$ff",0x07)
print_op("ld e,$ff",0x08)
print_op("ld h,$ff",0x09)
print_op("ld l,$ff",0x0a)
print_op("ld bc,$ffff",0x0b)
print_op("ld de,$ffff",0x0c)
print_op("ld hl,$ffff",0x0d)
print_op("ld a,($ffff)",0x0e)
print_op("ld b,($ffff)",0x0f)
print_op("ld c,($ffff)",0x10)
print_op("ld d,($ffff)",0x11)
print_op("ld e,($ffff)",0x12)
print_op("ld h,($ffff)",0x13)
print_op("ld l,($ffff)",0x14)
print_op("ld ($ffff),a",0x15)
print_op("push bc",0x16)
print_op("push de",0x17)
print_op("push hl",0x18)
print_op("pop bc",0x19)
print_op("pop de",0x1a)
print_op("pop hl",0x1b)
print_op("inc a",0x1c)
print_op("sub $ff",0x1d)

