import parse, emulakcompile

instr = parse.InstructionList("instructions.txt")

code = """.section "Main"
.org $0000
.set base_address $6000
Loop:
jp Loop
.orgsection "Other" $0009
Test:
ret
ld a,(Test)"""

e = emulakcompile.parse_text(code,"inline",instr)

print "----"

for section in e:
	print("Name: {}; Size: {!s}; File: {}; Offset: ${!s};".format(section.name,len(section.bytes),section.filename,hex(section.loc)[2:].zfill(4)))
	print(" ".join(hex(x)[2:].zfill(2) for x in section.bytes))
	print("----")
