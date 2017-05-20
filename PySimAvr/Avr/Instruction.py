####################################################################################################
# 
# PySimAvr - Python binding to simavr.
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

"""This modules implements an assembler and disassembler for the AVR instruction set.

The AVR instruction set is described by a JSON file containing information from the Atmel Datasheet
8-bit AVR Instruction Set 0856I-AVR-07/10.

The instructions are stored in the dictionnary *instructions*.

This snippet shows how to generate and decode a bytecode for a particular instruction::

  ldd = instructions['LDD'].first_opcode
  bytecode = ldd.encode(d=0xA, q=0x2A)
  operands = ldd.decode(bytecode)

Registers and Operands:

* Rd: Destination (and source) register in the Register File 
* Rr: Source register in the Register File 
* R: Result after instruction is executed 
* K: Constant data 
* k: Constant address 
* b: Bit in the Register File or I/O Register (3-bit) 
* s: Bit in the Status Register (3-bit) 
* X,Y,Z: Indirect Address Register (X=R27:R26, Y=R29:R28 and Z=R31:R30) 
* A: I/O location address 
* q: Displacement for direct addressing (6-bit)

Operation Language:

The operations are described using a mini-language whose the syntax is:

``R(i)``
  ith bit of R

``Rd(3..0)``
   nibble

``xh:xl``
  form a 16-bit value from two 8-bit values

``(R)``
  indirect addressing: value at address

``I/O(P, b)``
  bth bit of port P

``STACK``
  stack

``<-``
  set the destination

``+ -``
  arithmetic operation: addition and subtraction

``& | x <<``
  logical operation: and, or, xor, shift

``if (<expression> == 0) then ...``
  condition

``or``
  alternative

``<expression>, <expression>``
  multi-operation

.. note:: A parser like `ply <http://www.dabeaz.com/ply>`_ can easily parse and run this
  mini-language.  Same apply for operation on the status register.  Such feature is quite
  interesting for unit-tests since we can directly execute what is written in the datasheet.  We
  could also auto-generate C code.  The unit-tests of simulavr are mandatory but the implementation
  is really too verbose, we can something more clever.  We just have to provide code for the most
  complex or special instructions.

"""

####################################################################################################

import collections
import itertools
import json
import os

####################################################################################################

from PySimAvr.Math.Interval import IntervalInt

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

    def is_compatible(self, other):
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
        return int(self.opcode, 2)
        # return sum([int(c) << i for i, c in enumerate(reversed(self.opcode))])        

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

    def is_compatible(self, other):
        return isinstance(other, self.__class__) and self.letter == other.letter

    ##############################################

    def encode(self, value):
        return ((value >> self.operand_shift) & self.mask) << self.opcode_shift

    ##############################################

    def decode(self, bytecode):
        return ((bytecode >> self.opcode_shift) & self.mask) << self.operand_shift
    
####################################################################################################

class Opcode(object):

    """ This class implements an AVR opcode. """
    
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
            if not chunks or not chunks[-1].is_compatible(chunk):
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
    def mnemonic(self):
        return self.instruction.mnemonic
    
    ##############################################

    @property
    def no_operand(self):
        return self.mask == 0xFFFF

    ##############################################

    def encode(self, **args):

        """Generate the bytecode for this opcode.

        The operands must be passed as key-value pairs.

        """
        
        bytecode = self.opcode
        for operand, chunks in self.opcode_operands.items():
            for chunk in chunks:
                bytecode += chunk.encode(args[operand])
        return bytecode

    ##############################################

    def decode(self, bytecode):

        """Decode the bytecode corresponding to this opcode.

        Return an operand dictionnary.

        """
        
        operands = {operand:0 for operand in self.opcode_operands}
        for operand, chunks in self.opcode_operands.items():
            for chunk in chunks:
                operands[operand] += chunk.decode(bytecode)
        return operands

    ##############################################

    def opcode_intervals(self):

        # Fixme: opcodes with low bits (e.g. xxxx x100) introduces steps
        #   else right ???
        #   => fill an array of size 65536 ... ???
        
        last_chunk = self.chunks[-1]
        if isinstance(last_chunk, OpcodeChunk):
            opcode_step = int(last_chunk)
            print('low bit opcode', last_chunk, int(last_chunk))
        else:
            opcode_step = 0
            
        # Merge contiguous operand bits
        operand_intervals = []
        for chunk in reversed(self.chunks):
            if isinstance(chunk, OperandChunk):
                inf = chunk.opcode_shift
                interval = IntervalInt(inf, inf + len(chunk) -1)
                # print(chunk, chunk.opcode_shift, len(chunk), interval)
                if operand_intervals and interval.inf == operand_intervals[-1].sup +1:
                    operand_intervals[-1] |= interval
                else:
                    operand_intervals.append(interval)
        # print([str(x) for x in operand_intervals])

        # Compute a cartesian product of the operand chuncks
        bytecode_intervals = []
        for combination in itertools.product((0, 1), repeat=len(operand_intervals)):
            bytecode_inf = bytecode_sup = self.opcode
            for weight, interval in zip(combination, reversed(operand_intervals)):
                if weight:
                    # case where bits are unset is take into account by a null weight
                    bytecode_inf += 2**interval.inf # lower chunk bit is set
                    bytecode_sup += 2**(interval.sup +1) - 2**interval.inf # all chunk bits are set
            prefix = str(combination)
            print(prefix, bin(bytecode_inf), bytecode_inf)
            print(' '*len(prefix), bin(bytecode_sup), bytecode_sup)
            interval = IntervalInt(bytecode_inf, bytecode_sup)
            if bytecode_intervals and interval.inf <= bytecode_intervals[-1].sup +1:
                bytecode_intervals[-1] |= interval
            else:
                bytecode_intervals.append(interval)
        print([str(x) for x in bytecode_intervals])

        return bytecode_intervals

####################################################################################################

class Instruction(object):

    """ This class implements an AVR instruction.

    An instruction can have one or several associated opcodes.
    """
    
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

    def __repr__(self):
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

_json_path = os.path.join(os.path.dirname(__file__), 'opcodes.json')

#: Dictionnary providing the :class:`Instruction` instances for the AVR instruction set.
instructions = collections.OrderedDict()
with open(_json_path) as f:
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
