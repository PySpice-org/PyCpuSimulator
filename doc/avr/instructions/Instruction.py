####################################################################################################

# Registers and Operands
# 
# Rd: Destination (and source) register in the Register File 
# Rr: Source register in the Register File 
# R: Result after instruction is executed 
# K: Constant data 
# k: Constant address 
# b: Bit in the Register File or I/O Register (3-bit) 
# s: Bit in the Status Register (3-bit) 
# X,Y,Z: Indirect Address Register (X=R27:R26, Y=R29:R28 and Z=R31:R30) 
# A: I/O location address 
# q: Displacement for direct addressing (6-bit)

####################################################################################################

class OpcodeChunk(object):

    ##############################################

    def __init__(self, opcode):

        self.opcode = opcode

    ##############################################

    def __iadd__(self, other):

        self.opcode += other.opcode
        return self
        
    ##############################################

    def __len__(self):
        return len(self.opcode)

    ##############################################

    def __int__(self):
        return sum([int(c) << i for i, c in enumerate(reversed(self.opcode))])        

    ##############################################

    def __repr__(self):
        return str(self)
    
    ##############################################

    def __str__(self):
        return hex(int(self)) + " #{}".format(len(self)) 

    ##############################################

    def compatible(self, other):
        return isinstance(other, self.__class__)

    ##############################################

    @property
    def mask(self):
        return 2**len(self) -1

####################################################################################################
    
class OperandChunk(object):

    ##############################################

    def __init__(self, letter, count=1):

        self.letter = letter
        self.count = count
        
    ##############################################

    def __iadd__(self, opcode):

        self.count += opcode.count
        return self
        
    ##############################################

    def __len__(self):
        return self.count

    ##############################################

    def __repr__(self):
        return str(self)
    
    ##############################################

    def __str__(self):
        return self.letter + " #{}".format(self.count)

    ##############################################

    def compatible(self, other):
        return isinstance(other, self.__class__) and self.letter == other.letter

####################################################################################################

class Opcode(object):

    ##############################################

    def __init__(self, instruction, opcode):


        self.instruction = instruction
        self.opcode_string = opcode

        self._parse_opcode()
        
    ##############################################

    def _parse_opcode(self):

        opcode = ''.join(self.opcode_string.split(' '))

        self.opcode_size = len(opcode)
        if self.opcode_size not in (16, 32):
            raise ValueError('%s', opcode)

        self.chunks = chunks = []
        for c in opcode[:16]:
            if c in ('0', '1'):
                chunk = OpcodeChunk(c)
            else:
                chunk = OperandChunk(c)
            if not chunks or not chunks[-1].compatible(chunk):
                chunks.append(chunk)
            else:
                chunks[-1] += chunk

        if self.opcode_size == 32:
            self.operand_32 = opcode[16:]
        else:
            self.operand_32 = None
            
        self.opcode = 0
        self.mask = 0
        self.operand_pattern = ''
        shift = 16
        count = 0
        for chunk in self.chunks:
            count += len(chunk)
            shift -= len(chunk)
            if isinstance(chunk, OpcodeChunk):
                self.opcode += int(chunk) << shift
                self.mask += chunk.mask << shift
                self.operand_pattern += '_{}'.format(len(chunk))
            else:
                self.operand_pattern += '{}{}'.format(chunk.letter, len(chunk))
        if count != 16:
            print(self.chunks, self.operand_32)
            raise ValueError("%s %s", self.opcode_string, self.operand_pattern)

    ##############################################

    @property
    def no_operand(self):
        return self.mask == 0xFFFF
        
####################################################################################################

class Instruction(object):

    ##############################################

    def __init__(self, name, description, opcodes):

        self.name = name
        self.description = description

        self.opcodes = [Opcode(self, opcode) for opcode in opcodes]
        
    ##############################################

    def __str__(self):

        return self.name

    ##############################################

    @property
    def first_opcode(self):
        return self.opcodes[0]
    
    ##############################################

    @property
    def no_operand(self):
        return len(self.opcodes) == 1 and self.opcodes[0].no_operand

####################################################################################################

class DecisionTree(object):

    ##############################################

    def __init__(self, instructions):

        self._tree = {}
        self._build(instructions)
        self._simplify()
        
    ##############################################

    def _build(self, instructions):
        
        for instruction in instructions.values():
            for opcode in instruction.opcodes:
                keys = [opcode.opcode & mask for mask in (0xF000, 0x0F00, 0x00F0, 0x000F)]
                # print([hex(key) for key in keys])
                tree1 = self._tree.setdefault(keys[0], dict())
                tree2 = tree1.setdefault(keys[1], dict())
                tree3 = tree2.setdefault(keys[2], dict())
                tree3[keys[3]] = opcode

    ##############################################

    def _simplify(self):

        tree0 = self._tree
        for key0 in list(tree0):
            tree1 = self._tree[key0]
            len1 = len(tree1)
            for key1 in list(tree1):
                tree2 = tree1[key1]
                len2 = len(tree2)
                for key2 in list(tree2):
                    tree3 = tree2[key2]
                    len3 = len(tree3)
                    if len3 == 1:
                        key3 = list(tree3.keys())[0]
                        opcode = tree3[key3]
                        key23 = key2 + key3
                        if len2 == 1:
                            key123 = key1 + key23
                            if len1 == 1:
                                self._tree[key0 + key123] = opcode
                                if key123:
                                    del tree0[key0] # tree1
                            else:
                                tree1[key123] = opcode
                            if key23:
                                del tree1[key1] # tree2
                        else:
                            tree2[key23] = opcode
                        del tree2[key2] # tree3

    ##############################################

    def print_tree(self):
        
        self._print_tree(self._tree, 0)
        
    ##############################################

    def _print_tree(self, tree, level):

        indentation = " "*2*level
        for key in sorted(tree):
            item = tree[key]
            if isinstance(item, dict):
                print(indentation + "+ Ox{:04x}".format(key))
                self._print_tree(item, level+1)
            else:
                print(indentation + "+ Ox{:04x} Ox{:04x} {}".format(key, item.opcode, item.instruction))
                
####################################################################################################

import json
import collections

instructions = collections.OrderedDict()

with open('opcodes.json') as f:
    d = json.load(f)
    for name in sorted(d.keys()):
        description, opcodes = d[name]
        instructions[name] = Instruction(name, description, opcodes)

for instruction in instructions.values():
    print()
    print(instruction.name)
    for i, opcode in enumerate(instruction.opcodes):
        print("  {:2} 0x{:04x} 0x{:04x} | {} | {}".format(i,
                                                          opcode.opcode, opcode.mask,
                                                          opcode.opcode_string,
                                                          opcode.operand_pattern))

print("\nInstructions without operand:")
for instruction in instructions.values():
    # if instruction.no_operand:
    for opcode in instruction.opcodes:
        if opcode.no_operand:
            print('  {:6s} 0x{:04x}'.format(instruction.name, opcode.opcode))

print("\nOperand patterns:")
operand_patterns = {}
for instruction in instructions.values():
    for opcode in instruction.opcodes:
        if opcode.no_operand:
            continue
        if opcode.operand_pattern in operand_patterns:
            operand_patterns[opcode.operand_pattern] += 1
        else:
            operand_patterns[opcode.operand_pattern] = 1
for operand_pattern in sorted(operand_patterns):
    print('  {:16} {:3}'.format(operand_pattern, operand_patterns[operand_pattern]))

decision_tree = DecisionTree(instructions)
print("\nDecision Tree:")
decision_tree.print_tree()
        
####################################################################################################
# 
# End
# 
####################################################################################################
