import emulakcompile

e = emulakcompile.EmulakObjectFile([0x01,0x00,0x60],0,"test.asm")
with open("test.o","w") as f:
	e.dump(f)
