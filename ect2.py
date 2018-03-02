from emulakcompile import *

with open("test.o") as f:
	o = EmulakObjectFile.load(f)
rom = EmulakROM("test.bin",4)
o.insert(rom)
rom.end()
