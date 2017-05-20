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

import collections
import json
import os

####################################################################################################

class Chunk(object):

    ##############################################

    def __init__(self):

        self.opcode_shift = None

    ##############################################

    @property
    def mask(self):
        return 2**len(self) -1
        
####################################################################################################

class OpcodeChunk(Chunk):

    ##############################################

    def __init__(self, opcode):

        super(OpcodeChunk, self).__init__()
        self.opcode = opcode

    ##############################################

    def compatible(self, other):
        return isinstance(other, self.__class__)
        
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

####################################################################################################
    
class OperandChunk(Chunk):

    ##############################################

    def __init__(self, letter, count=1):

        super(OperandChunk, self).__init__()
        self.operand_shift = None
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

    ##############################################

    def encode(self, value):
        return ((value >> self.operand_shift) & self.mask) << self.opcode_shift

    ##############################################

    def decode(self, bytecode):
        return ((bytecode >> self.opcode_shift) & self.mask) << self.operand_shift
    
####################################################################################################

class Opcode(object):

    ##############################################

    def __init__(self, instruction, opcode,
                 operands=None, operation=None, flags=None, cycles=None):


        self.instruction = instruction
        self.opcode_string = opcode
        self.operands = operands
        self.operation = operation
        self.flags = flags
        self.cycles = cycles
        
        self._parse_opcode()
        
    ##############################################

    def _parse_opcode(self):

        """Parse the opcode bit pattern.

        Group the bit so as to make chuncks corresponding to the opcode and the operands.  Then
        generate an opcode mask, an opcode value and an operand bit pattern.

        """
        
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
        self.opcode_operands = {}
        operand_size = {}
        self.operand_pattern = ''
        shift = 16
        count = 0
        for chunk in self.chunks:
            count += len(chunk)
            shift -= len(chunk)
            chunk.opcode_shift = shift
            if isinstance(chunk, OpcodeChunk):
                self.opcode += int(chunk) << shift
                self.mask += chunk.mask << shift
                self.operand_pattern += '_{}'.format(len(chunk))
            else:
                if chunk.letter in operand_size:
                    self.opcode_operands[chunk.letter].append(chunk)
                    operand_size[chunk.letter] += len(chunk)
                else:
                    self.opcode_operands[chunk.letter] = [chunk]
                    operand_size[chunk.letter] = len(chunk)
                self.operand_pattern += '{}{}'.format(chunk.letter, len(chunk))
        if count != 16:
            # print(self.chunks, self.operand_32)
            raise ValueError("%s %s", self.opcode_string, self.operand_pattern)

        for operand, chunks in self.opcode_operands.items():
            for chunk in chunks:
                operand_size[operand] -= len(chunk)
                chunk.operand_shift = operand_size[operand]
        
    ##############################################

    def __repr__(self):
        return self.opcode_string
        
    ##############################################

    @property
    def no_operand(self):
        return self.mask == 0xFFFF

    ##############################################

    def encode(self, **args):

        bytecode = self.opcode
        for operand, chunks in self.opcode_operands.items():
            for chunk in chunks:
                bytecode += chunk.encode(args[operand])
        return bytecode

    ##############################################

    def decode(self, bytecode):

        operands = {operand:0 for operand in self.opcode_operands}
        for operand, chunks in self.opcode_operands.items():
            for chunk in chunks:
                operands[operand] += chunk.decode(bytecode)
        return operands
    
####################################################################################################

class Instruction(object):

    ##############################################

    def __init__(self, mnemonic, description, opcodes, alternate=None):

        self.mnemonic = mnemonic
        self.description = description
        self.alternate = alternate

        self.opcodes = [Opcode(self, **opcode_dict) for opcode_dict in opcodes]
        
    ##############################################

    def __str__(self):

        return self.mnemonic

    ##############################################

    @property
    def single_opcode(self):
        return len(self.opcodes) == 1
    
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

        """Build a decision tree using the mask.

        Diverge on mask's nibbles from the higher to the lowest.

        """
        
        for instruction in instructions.values():
            for opcode in instruction.opcodes:
                keys = [opcode.mask & nibble_mask
                        for nibble_mask in (0xF000, 0x0F00, 0x00F0, 0x000F)]
                tree1 = self._tree.setdefault(keys[0], dict())
                tree2 = tree1.setdefault(keys[1], dict())
                tree3 = tree2.setdefault(keys[2], dict())
                tree4 = tree3.setdefault(keys[3], dict())
                tree4[opcode.opcode] = opcode
        
    ##############################################

    def _simplify(self):

        """ Compress the tree when a branch is alone. """
        
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
        
        self._print_tree(self._tree)
        
    ##############################################

    def _print_tree(self, tree, stack=None):

        if stack is None:
            stack = []
        
        indentation = " "*4*len(stack)
        for key in sorted(tree, reverse=True):
            item = tree[key]
            if isinstance(item, dict):
                branch_stack = stack + [key]
                mask = sum(branch_stack)
                if key:
                    print(indentation + "& Ox{:04x}".format(mask))
                else:
                    print(indentation + "*& Ox{:04x}".format(mask))
                    # print(indentation + "True")
                self._print_tree(item, branch_stack)
            else:
                print(indentation + "= Ox{:04x} {}".format(item.opcode, item.instruction))

    ##############################################

    def print_masks(self):

        masks = set()
        for instruction in instructions.values():
            for opcode in instruction.opcodes:
                masks.add(opcode.mask)
        masks = sorted(masks, reverse=True)
        for mask in masks:
            print("  Ox{:04x} {}".format(mask, bin(mask)))
    
####################################################################################################

json_path = os.path.join(os.path.dirname(__file__), 'opcodes.json')

instructions = collections.OrderedDict()
with open(json_path) as f:
    json_dict = json.load(f)
    for mnemonic in sorted(json_dict.keys()):
        d = json_dict[mnemonic]
        instructions[mnemonic] = Instruction(mnemonic,
                                             description=d['description'],
                                             alternate=d.get('alternate', None),
                                             opcodes=d['operations'])

####################################################################################################
# 
# End
# 
####################################################################################################
