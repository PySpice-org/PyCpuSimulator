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

"""This modules implements an assembler and disassembler for instruction set.

The instructions are stored in the dictionnary *instructions*.

This snippet shows how to generate and decode a bytecode for a particular instruction::

  ldd = instructions['LDD'].first_opcode
  bytecode = ldd.encode(d=0xA, q=0x2A)
  operands = ldd.decode(bytecode)

"""

####################################################################################################

import collections
import itertools
import logging

import yaml

import numpy as np

####################################################################################################

from PySimAvr.Math.Interval import IntervalInt
from PySimAvr.Tools.BinaryNumber import sup_for_nbits

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Chunk(object):

    ##############################################

    def __init__(self):

        #! Shift in the opcode
        self._opcode_shift = None

    ##############################################

    @property
    def mask(self):
        """ Return a mask of 1 for the chunk length. """
        return sup_for_nbits(len(self))

####################################################################################################

class OpcodeChunk(Chunk):

    ##############################################

    def __init__(self, opcode):

        super(OpcodeChunk, self).__init__()
        self._opcode = opcode

    ##############################################

    def __len__(self):
        return len(self._opcode)

    ##############################################

    def __int__(self):
        return int(self._opcode, 2)

    ##############################################

    def __repr__(self):
        return str(self)

    ##############################################

    def __str__(self):
        return hex(int(self)) + " #{}".format(len(self))

    ##############################################

    def __iadd__(self, other):

        self._opcode += other._opcode
        return self

    ##############################################

    def is_compatible(self, other):
        return isinstance(other, self.__class__)

####################################################################################################

class OperandChunk(Chunk):

    ##############################################

    def __init__(self, letter, count=1):

        super(OperandChunk, self).__init__()
        #! Shift in the operand
        self._operand_shift = None
        self._letter = letter
        self._count = count

    ##############################################

    def __len__(self):
        return self._count

    ##############################################

    def __repr__(self):
        return str(self)

    ##############################################

    def __str__(self):
        return self._letter + " #{}".format(self._count)

    ##############################################

    def __iadd__(self, opcode):

        self._count += opcode._count
        return self

    ##############################################

    def is_compatible(self, other):
        return isinstance(other, self.__class__) and self._letter == other._letter

    ##############################################

    def encode(self, value):
        return ((value >> self._operand_shift) & self.mask) << self._opcode_shift

    ##############################################

    def decode(self, bytecode):
        return ((bytecode >> self._opcode_shift) & self.mask) << self._operand_shift

####################################################################################################

class Opcode(object):

    """ This class implements an AVR opcode. """

    ##############################################

    def __init__(self, instruction, opcode,
                 operands=None, operation=None, flags=None, cycles=None):

        self._instruction = instruction
        self._opcode_string = opcode
        self._operands = operands
        self._operation = operation
        self._flags = flags
        self._cycles = cycles

        self._parse_opcode()

    ##############################################

    @property
    def instruction(self):
        return self._instruction

    @property
    def mnemonic(self):
        return self._instruction.mnemonic

    @property
    def opcode_string(self):
        return self._opcode_string

    @property
    def cycles(self):
        return self._cycles

    @property
    def opcode_size(self):
        return self._opcode_size

    @property
    def opcode(self):
        return self._opcode

    @property
    def mask(self):
        return self._mask

    @property
    def operation(self):
        return self._operation

    @property
    def operand_pattern(self):
        return self._operand_pattern

    @property
    def opcode_operands(self):
        return self._opcode_operands

    ##############################################

    @property
    def no_operand(self):
        return self._mask == 0xFFFF

    ##############################################

    def __repr__(self):
        return self._opcode_string

    ##############################################

    def _parse_opcode(self):

        """Parse the opcode bit pattern.

        Opcode bits are represented by {0, 1} and operand bits by a letter.

        Group the bit so as to make chuncks corresponding to the opcode and the operands.  Then
        generate an opcode mask, an opcode value and an operand bit pattern.

        """

        opcode = ''.join(self._opcode_string.split(' '))

        self._opcode_size = len(opcode)
        if self._opcode_size not in (16, 32):
            raise ValueError('%s', opcode)

        self._chunks = chunks = []
        for c in opcode[:16]:
            if c in ('0', '1'):
                chunk = OpcodeChunk(c)
            else:
                chunk = OperandChunk(c)
            if not chunks or not chunks[-1].is_compatible(chunk):
                chunks.append(chunk)
            else:
                chunks[-1] += chunk

        if self._opcode_size == 32:
            self._operand_32 = opcode[16:]
        else:
            self._operand_32 = None

        #! Opcode value
        self._opcode = 0
        #! Opcode mask
        self._mask = 0
        self._opcode_pattern = ''
        #! Run length encoding of the operand pattern where opcode bit are represented by '_'
        self._operand_pattern = ''
        self._opcode_operands = {}

        operand_size = {}
        count = 0
        shift = 16
        for chunk in self._chunks:
            count += len(chunk)
            shift -= len(chunk)
            chunk._opcode_shift = shift
            if isinstance(chunk, OpcodeChunk):
                self._opcode += int(chunk) << shift
                self._mask += chunk.mask << shift
                self._opcode_pattern += chunk._opcode
                self._operand_pattern += '_{}'.format(len(chunk))
            else:
                chunk_length = len(chunk)
                if chunk._letter in operand_size:
                    self._opcode_operands[chunk._letter].append(chunk)
                    operand_size[chunk._letter] += chunk_length
                else:
                    self._opcode_operands[chunk._letter] = [chunk]
                    operand_size[chunk._letter] = chunk_length
                self._opcode_pattern += '_{}'.format(chunk_length)
                self._operand_pattern += '{}{}'.format(chunk._letter, chunk_length)
        if count != 16:
            # print(self._chunks, self._operand_32)
            raise ValueError("%s %s", self._opcode_string, self._operand_pattern)
        self._number_of_operand_bits = sum(operand_size.values())
        for operand, chunks in self._opcode_operands.items():
            for chunk in chunks:
                operand_size[operand] -= len(chunk)
                chunk._operand_shift = operand_size[operand]

    ##############################################

    def encode(self, **args):

        """Generate the bytecode for this opcode.

        The operands must be passed as key-value pairs.

        """

        bytecode = self._opcode
        for operand, chunks in self._opcode_operands.items():
            for chunk in chunks:
                bytecode += chunk.encode(args[operand])
        return bytecode

    ##############################################

    def decode(self, bytecode):

        """Decode the bytecode corresponding to this opcode.

        Return an operand dictionnary.

        """

        operands = {operand:0 for operand in self._opcode_operands}
        for operand, chunks in self._opcode_operands.items():
            for chunk in chunks:
                operands[operand] += chunk.decode(bytecode)
        return operands

    ##############################################

    def _merge_operands(self):

        """ Merge contiguous operand bits """

        operand_intervals = []
        for chunk in reversed(self._chunks):
            if isinstance(chunk, OperandChunk):
                inf = chunk._opcode_shift
                interval = IntervalInt(inf, inf + len(chunk) -1)
                # print(chunk, chunk._opcode_shift, len(chunk), interval)
                if operand_intervals and interval.inf == operand_intervals[-1].sup +1:
                    operand_intervals[-1] |= interval
                else:
                    operand_intervals.append(interval)
        # print([str(x) for x in operand_intervals])
        
        return operand_intervals

    ##############################################

    def iter_on_bytecodes(self):

        operand_intervals = self._merge_operands()
        operand_shift_mask = []
        operand_shift = 0
        for interval in operand_intervals:
            number_of_bits = interval.length()
            operand_shift_mask.append((operand_shift, sup_for_nbits(number_of_bits), interval.inf))
            operand_shift += number_of_bits
        for operand in range(2**self._number_of_operand_bits):
            bytecode = self._opcode
            for operand_shift, mask, opcode_shift in operand_shift_mask:
                value = ((operand >> operand_shift) & mask) << opcode_shift
                bytecode += value
            yield bytecode

    ##############################################

    def opcode_intervals(self):

        # Opcodes with less significant bits (e.g. xxxx x100) introduces steps
        if self._mask & 1:
            raise NotImplementedError

        last_chunk = self._chunks[-1]
        if isinstance(last_chunk, OpcodeChunk):
            opcode_step = int(last_chunk)
            print('low bit opcode', last_chunk, int(last_chunk))
        else:
            opcode_step = 0

        operand_intervals = self._merge_operands()

        # Compute a cartesian product of the operand chuncks
        bytecode_intervals = []
        for combination in itertools.product((0, 1), repeat=len(operand_intervals)):
            bytecode_inf = bytecode_sup = self._opcode
            for weight, interval in zip(combination, reversed(operand_intervals)):
                if weight:
                    # case where bits are unset is take into account by a null weight
                    bytecode_inf += 2**interval.inf # lower chunk bit is set
                    bytecode_sup += 2**(interval.sup +1) - 2**interval.inf # all chunk bits are set
            # prefix = str(combination)
            # print(prefix, bin(bytecode_inf), bytecode_inf)
            # print(' '*len(prefix), bin(bytecode_sup), bytecode_sup)
            interval = IntervalInt(bytecode_inf, bytecode_sup)
            if bytecode_intervals and interval.inf <= bytecode_intervals[-1].sup +1:
                bytecode_intervals[-1] |= interval
            else:
                bytecode_intervals.append(interval)
        # print([str(x) for x in bytecode_intervals])
        
        return bytecode_intervals

####################################################################################################

class InstructionBase(object):

    ##############################################

    def __init__(self, mnemonic, description):

        self._mnemonic = mnemonic
        self._description = description

    ##############################################

    @property
    def mnemonic(self):
        return self._mnemonic

    @property
    def description(self):
        return self._description

    ##############################################

    def __str__(self):
        return self._mnemonic

    ##############################################

    def __repr__(self):
        return self._mnemonic

####################################################################################################

class Instruction(InstructionBase):

    """ This class implements an AVR instruction.

    An instruction can have one or several associated opcodes.
    """

    ##############################################

    def __init__(self, mnemonic, description, opcodes, alternate=None):

        super(Instruction, self).__init__(mnemonic, description)
        self._alternate = alternate

        self._opcodes = [Opcode(self, **opcode_dict) for opcode_dict in opcodes]

    ##############################################

    @property
    def opcodes(self):
        return iter(self._opcodes)

    @property
    def alternate(self):
        return self._alternate

    ##############################################

    @property
    def single_opcode(self):
        return len(self._opcodes) == 1

    ##############################################

    @property
    def first_opcode(self):
        return self._opcodes[0]

    ##############################################

    @property
    def no_operand(self):
        return len(self._opcodes) == 1 and self._opcodes[0].no_operand

####################################################################################################

class InstructionAlias(InstructionBase):

    ##############################################

    def __init__(self, mnemonic, description, alias_of, alias_substitution):

        super(InstructionAlias, self).__init__(mnemonic, description)
        self._alias_of = alias_of
        self._alias_substitution = alias_substitution

    ##############################################

    @property
    def opcodes(self):
        return []

####################################################################################################

class DecodeError(NameError):
    pass

####################################################################################################

class DecisionTreeNode(object):

    ##############################################

    def __init__(self):

        self._mask = None
        self._branches = {}
        self._default = None

    ##############################################

    def decode(self, bytecode, default_node=None):

        # keep track of the default node
        if self._default is not None:
            default_node = self._default

        try:
            key = bytecode & self._mask
            node = self._branches[key]
            if isinstance(node, Opcode):
                return node
            else:
                return node.decode(bytecode, default_node)
        except KeyError:
            if default_node is not None:
                # default_node should be a singleton (cf. Theiling p2)
                return default_node
            else:
                raise DecodeError('Cannot decode bytecode')

    ##############################################

    def print(self, level=0):

        prefix = '    '*level
        print(prefix + "Node mask {:016b}  0x{:04x}".format(self._mask, self._mask))
        print(prefix + '  default: ' + str(self._default))
        for label, node in self._branches.items():
            print(prefix + '  {:016b}  0x{:04x}'.format(label, label))
            if isinstance(node, DecisionTreeNode):
                node.print(level +1)
            else:
                opcode = node
                string_format = prefix + "    > {:016b}  0x{:04x}  {:016b}  {:6}  {}"
                print(string_format.format(opcode.opcode,
                                           opcode.opcode,
                                           opcode.mask,
                                           opcode.instruction.mnemonic,
                                           opcode))

####################################################################################################

class DecisionTree(object):

    """This class implements a decision tree to decode opcodes of an instruction set.

    The algorithm is described in the paper Generating Decision Trees for Decoding Binaries, Henrik
    Theiling.

    .. warning:: Default node was not tested.

    """

    _logger = _module_logger.getChild('DecisionTree')

    ##############################################

    def __init__(self, instruction_set):

        self._instruction_set = instruction_set

        opcode_set = instruction_set.opcode_set()

        # opcode_set.sort(key=lambda opcode: opcode.opcode)
        # for opcode in opcode_set:
        #     string_format = "{:016b}  0x{:04x}  {:016b}  {:6}  {}"
        #     print(string_format.format(opcode.opcode, opcode.opcode,
        #                                opcode.mask,
        #                                opcode.instruction.mnemonic, opcode))
        
        self._root = self._make_tree(opcode_set, gmask=0xFFFF)

    ##############################################

    @staticmethod
    def _get_default(opcode_set, gmask):

        # Compute the set of bits patterns that have empty remaining bit masks
        singleton = [opcode for opcode in opcode_set
                     if not opcode.mask & gmask]
        if len(singleton) != 1:
            raise NameError('Not a singleton')
        singleton = singleton[0]
        # print('singleton:', singleton)

        # Get a mask
        mask = gmask
        opcode_subset = []
        for opcode in opcode_set:
            if opcode is not singleton:
                mask &= opcode.mask
                opcode_subset.append(opcode)
        if not mask:
            raise NameError('Null mask')
        # print('default mask:', bin(mask))

        return singleton, opcode_subset, mask

    ##############################################

    def _partitions(self, opcode_set, mask):

        """Group opcodes having the same bit values for the significant bits defined by mask."""

        sorted_opcode_set = sorted(opcode_set, key=lambda opcode: opcode.opcode & mask)

        # print('\nPartitioning of the opcode set with mask:\n{:016b}'.format(mask))
        partitions = []
        partition = None
        partition_bit_values = None
        for opcode in sorted_opcode_set:
            opcode_bit_values = opcode.opcode & mask
            if opcode_bit_values == partition_bit_values:
                partition.append(opcode)
            else:
                if partition_bit_values is not None:
                    partitions.append(partition)
                # print('  New partition')
                partition = [opcode]
                partition_bit_values = opcode_bit_values
            # coloured_opcode = format_and_colour_with_mask(opcode.opcode, mask, 16)
            # coloured_mask = format_and_colour_with_mask(opcode.mask, mask, 16)
            # print("{}  {}  {:6}  {}".format(coloured_opcode,
            #                                 coloured_mask,
            #                                 opcode.instruction.mnemonic, opcode))
        partitions.append(partition)

        return partitions

    ##############################################

    def _make_tree(self, opcode_set, gmask, level=0):

        # print('\n\nMake Tree mask level {} {:016b}'.format(level, gmask))
        
        # Compute a bit mask of bits that are significant for all bit patterns
        mask = gmask
        for opcode in opcode_set:
            # print(bin(opcode.mask))
            mask &= opcode.mask
        # print('mask:', bin(mask))
        
        # Possibly terminate, must be singleton
        if not mask and len(opcode_set) == 1:
            # print('Terminate for null mask and singleton')
            return opcode_set[0]

        # Construct an new node
        node = DecisionTreeNode()

        # Decide about default node
        if not mask:
            singleton, opcode_set, mask = self._get_default(opcode_set, gmask)
            node.default = singleton

        # label the current node
        node._mask = mask

        # make partition of the opcode set using mask
        partitions = self._partitions(opcode_set, mask)

        # recurse on subsets
        for partition in partitions:
            label = partition[0].opcode & mask
            partition_node = self._make_tree(partition, gmask - mask, level +1)
            node._branches[label] = partition_node

        # Return the new node
        return node

    ##############################################

    def decode(self, bytecode):

        return self._root.decode(bytecode)

    ##############################################

    def brut_force_check(self):

        """ Try to decode all the bytecodes and check the result. """

        # print('Brut force check:')
        for opcode, bytecode in self._instruction_set.yield_bytecode():
            decoded_opcode = self.decode(bytecode)
            if decoded_opcode is not opcode:
                raise NameError('Decision tree check failed for opcode {}'.format(opcode))
            # else:
            #     print('  {} passed'.format(opcode))

    ##############################################

    def print(self):

        print()
        self._root.print()

####################################################################################################

class InstructionSet(collections.OrderedDict):

    ##############################################

    def __init__(self, yaml_path=None):

        super(InstructionSet, self).__init__()

        self._decision_tree = None

        if yaml_path is not None:
            self._load_yaml(yaml_path)

    ##############################################

    def _load_yaml(self, yaml_path):

        with open(yaml_path) as f:
            yaml_dict = yaml.load(f)
        for mnemonic in sorted(yaml_dict.keys()):
            d = yaml_dict[mnemonic]
            if 'alias_of' in d:
                instruction = InstructionAlias(mnemonic,
                                               description=d['description'],
                                               alias_of=d['alias_of'],
                                               alias_substitution=d.get('alias_substitution', None))
            else:
                instruction = Instruction(mnemonic,
                                          description=d['description'],
                                          alternate=d.get('alternate', None),
                                          opcodes=d['operations'])
            self[mnemonic] = instruction

    ##############################################

    @property
    def decision_tree(self):

        if self._decision_tree is None:
            self._decision_tree = DecisionTree(self)
        return self._decision_tree

    ##############################################

    def iter_on_instructions(self):

        for instruction in self.values():
            if isinstance(instruction, Instruction):
                yield instruction

    ##############################################

    def opcode_set(self):

        opcode_set = []
        for instruction in self.iter_on_instructions():
            opcode_set.extend(instruction.opcodes)
        return opcode_set

    ##############################################

    def yield_bytecode(self):

        for instruction in self.iter_on_instructions():
            for opcode in instruction.opcodes:
                for bytecode in opcode.iter_on_bytecodes():
                    yield opcode, bytecode

    ##############################################

    def check_for_clash(self, verbose=False):

        number_of_bytecodes = 2**16

        bytecode_array = np.zeros(number_of_bytecodes, dtype=np.uint64)
        opcode_map = {}
        opcode_clash = collections.OrderedDict()
        for instruction in self.iter_on_instructions():
            for opcode in instruction.opcodes:
                opcode_map[id(opcode)] = opcode
                for bytecode in opcode.iter_on_bytecodes():
                    if bytecode_array[bytecode]:
                        opcode_clash[id(opcode)] = bytecode_array[bytecode]
                        # opcode0 = opcode_map[bytecode_array[bytecode]]
                        # instruction0 = opcode0.instruction
                        # message = "Clash for  {} {}  with  {} {}  for bytecode  {}"
                        # print(message.format(instruction.mnemonic, opcode.opcode_string,
                        #                      instruction0.mnemonic, opcode0.opcode_string,
                        #                      format_as_nibble(bytecode)))
                    else:
                        bytecode_array[bytecode] = id(opcode)

        for opcode_id1, opcode_id2 in opcode_clash.items():
            opcode1 = opcode_map[opcode_id1]
            instruction1 = opcode1.instruction
            opcode2 = opcode_map[opcode_id2]
            instruction2 = opcode2.instruction
            message = "Clash for  {} {}  with  {} {}"
            print(message.format(instruction1.mnemonic, opcode1.opcode_string,
                                 instruction2.mnemonic, opcode2.opcode_string))

        if verbose:
            free_bytecodes = np.where(bytecode_array == 0)[0]
            free_intervals = []
            if free_bytecodes.shape[0]:
                inf = sup = free_bytecodes[0]
                for bytecode in free_bytecodes[1:]:
                    if bytecode == sup +1:
                        sup = bytecode
                    else:
                        free_intervals.append(IntervalInt(inf, sup))
                        inf = sup = bytecode
                free_intervals.append(IntervalInt(inf, sup))

            print('Free bytecodes:')
            bytecode_count = 0
            histogram = {}
            for interval in free_intervals:
                interval_length = interval.length()
                if interval_length in histogram:
                    histogram[interval_length] += 1
                else:
                    histogram[interval_length] = 1
                if interval_length > 1:
                    print("  - {:016b}\n    {:016b} #{}".format(interval.inf,
                                                                interval.sup - interval.inf,
                                                                interval_length))
                else:
                    print("  - {:016b}".format(interval.inf))
                bytecode_count += interval_length
            print("{} free bytecodes ({:.1f} %)".format(bytecode_count, 100*bytecode_count/number_of_bytecodes))
            print("\nRange distribution:")
            for interval_length in sorted(histogram):
                print("  {:4} × {:4} bytecodes".format(histogram[interval_length], interval_length))

####################################################################################################
#
# End
#
####################################################################################################
