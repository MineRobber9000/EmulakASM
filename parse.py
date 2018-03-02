# uncompyle6 version 2.16.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 20 2017, 18:23:56) 
# [GCC 5.4.0 20160609]
# Embedded file name: parse.py
# Compiled at: 2018-03-01 18:33:34
import re
HEX_CHARACTER_RE_CLASS = '[0-9A-Fa-f]'

class Instruction:
    def __init__(self, id, line):
        if type(id) != int:
            id = int(id, 16)
        self.id = id
        self.desc = line
        self.format_str = line.replace('(', '\\(').replace(')', '\\)').replace(' ', '[\\s]*').replace('a16', ('\\$({}{}{}{})').format(*([HEX_CHARACTER_RE_CLASS] * 4))).replace('d8', ('\\$({}{})').format(*([HEX_CHARACTER_RE_CLASS] * 2))).replace('d16', ('\\$({}{}{}{})').format(*([HEX_CHARACTER_RE_CLASS] * 4)))


class InstructionList:

    def __init__(self, filename):
        lines = []
        with open(filename) as (f):
            lines = [ l.strip().split(' - ') for l in f ]
        lines = filter(lambda x: x[1] != 'JAM', lines)
        self.opcodes = dict()
        for line in lines:
            self.opcodes[int(line[0], 16)] = Instruction(*line)


def parse_opcode_num(instr, op):
    op = op.upper()
    for k in instr.opcodes:
        if re.match(instr.opcodes[k].format_str, op):
            return k


def parse_opcode(instr, num, op):
    op = op.upper()
    fms = instr.opcodes[num].format_str
    m = re.match(fms, op)
    assert m is not None, ('Opcode "{}" is not of ID 0x{} ({})').format(op, hex(instr.opcodes[num].id)[2:].zfill(2), instr.opcodes[num].desc)
    if len(m.groups()):
        arg = m.group(1)
        if len(arg) == 2:
            return [num, int(arg, 16)]
        if len(arg) == 4:
            return [num, int(arg[2:4], 16), int(arg[:2], 16)]
    return [num]

class Section:

    def __init__(self, name, loc, filename, bytes):
        self.name = name
        self.loc = loc
        self.filename = filename
        self.bytes = bytes

    def gen_objectfile_keywords(self):
        return dict(bytes=self.bytes, offset=self.loc, section_name=self.name, filename=self.filename)
