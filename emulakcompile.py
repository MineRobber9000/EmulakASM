import cPickle, parse, re, copy

class EmulakAssemblerException(Exception):
	pass

class EmulakObjectFile:
	def __init__(self,bytes,offset,section_name,filename):
		self.bytes = bytes
#		self.size = len(bytes)
		self.offset = offset
		self.filename = filename
		self.section_name = section_name

	@property
	def size(self):
		return len(self.bytes)

	def insert(self,rom):
		for i in range(self.offset,self.offset+self.size):
			if i>=len(rom.bytes):
				raise EmulakAssemblerException("Section \"{}\" (from \"{}\") cannot be inserted into ROM \"{}\": ROM too small".format(self.section_name,self.filename,rom.filename))
		rom.bytes[self.offset:self.offset+self.size] = self.bytes

	def dump(self,file):
		cPickle.dump(self,file)

	@classmethod
	def load(cls,file):
		return cPickle.load(file)

class EmulakROM:
	def __init__(self,filename,size):
		self.filename = filename
		self.bytes = [0]*size
		self.size = size

	def end(self):
		with open(self.filename,"w") as f:
			f.write(bytearray(self.bytes))

DIRECTIVE = re.compile(r"\.([A-Za-z]+) (.+)")

def parse_text(t,filename,instr):
	lines = [l.rstrip() for l in t.split("\n")]
	filter(None,lines)
	try:
		assert lines[0].startswith(".section") or lines[0].startswith(".org") or lines[0].startswith(".orgsection")
		if not lines[0].startswith(".orgsection"):
			assert lines[1].startswith(".section") or lines[1].startswith(".org")
	except AssertionError:
		return []
	ret = []
	i = 0
	section_title = ""
	offset = 0
	section = None
	base_address = 0
	base_offset = 0
	labels = dict()
	o_or_s = 0
	while i < len(lines):
		if DIRECTIVE.match(lines[i]):
			m = DIRECTIVE.match(lines[i])
			name, args = m.groups()
			if name not in ('org','section','orgsection','set'):
				raise EmulakAssemblerException("Invalid directive {}!".format(lines[i]))
			if name=="org":
				if not lines[i+1].startswith(".section"):
					if not (o_or_s==2):
						raise EmulakAssemblerException("Using org without matching section!")
				else:
					o_or_s = 1
				#print "$({}{}{}{})".format(*[parse.HEX_CHARACTER_RE_CLASS]*4)
				om = re.match(r"\$({}{}{}{})".format(*[parse.HEX_CHARACTER_RE_CLASS]*4),args)
				if om:
					offset = int(om.group(1),16)
				else:
					raise EmulakAssemblerException("Invalid offset in org directive! ({})".format(args))
				if o_or_s==2:
					if section is not None:
						ret.append(copy.copy(section))
					section = parse.Section(section_title,offset,filename,[])
					base_offset = offset
					o_or_s=0
			elif name=="section":
				if not lines[i+1].startswith(".org"):
					if not (o_or_s==1):
						raise EmulakAssemblerException("Using org without matching section!")
				else:
					o_or_s = 2
				section_title = eval(args)
				if o_or_s==1:
					if section is not None:
						ret.append(copy.copy(section))
					section = parse.Section(section_title,offset,filename,[])
					base_offset = offset
					o_or_s = 0
			elif name=="orgsection":
				if section is not None:
					ret.append(copy.copy(section))
				args = args.split()
				om = re.match("\$({}{}{}{})".format(*[parse.HEX_CHARACTER_RE_CLASS]*4),args[1])
				if om:
					offset = int(om.group(1),16)
				else:
					raise EmulakAssemblerException("Invalid offset in orgsection directive!")
				section = parse.Section(eval(args[0]),offset,filename,[])
				base_offset = offset
			elif name=="set":
				args = args.split()
				if args[0] not in ("base_address"):
					raise EmulakAssemblerException("Invalid setting {}!".format(args[0]))
				if args[0] == "base_address":
					om = re.match("\$({}{}{}{})".format(*[parse.HEX_CHARACTER_RE_CLASS]*4),args[1])
					if om:
						base_address = int(om.group(1),16)
					else:
						raise EmulakAssemblerException("Invalid offset in orgsection directive!")
			i += 1
		elif lines[i].endswith(":"):
			labels[lines[i][:-1]]=base_address+base_offset
			print lines[i][:-1]
			i+=1
		else:
			line = lines[i]
			if not line:
				i+=1
				continue
			for label in labels:
				line = line.replace(label,"$"+(hex(labels[label])[2:].zfill(4)))
			id = parse.parse_opcode_num(instr,line)
			if not id:
				raise EmulakAssemblerException("Syntax error: {}".format(line))
			bytes = parse.parse_opcode(instr,id,line)
			section.bytes.extend(bytes)
			base_offset+=len(section.bytes)
			i += 1
	ret.append(section)
	return ret

def parse_file(instr,filename):
	with open(filename) as f:
		return parse_text(f.read(),filename,instr)

#if __name__=="__main__":
#	e = EmulakObjectFile([0x01,0x00,0x60],0,"test.asm")
#	with open("test.o","w") as f:
#		e.dump(f)
