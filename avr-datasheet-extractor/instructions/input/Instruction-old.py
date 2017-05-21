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

    def compatible(self, other):
        return isinstance(other, self.__class__)

####################################################################################################

class OpcodeOperand(object):

    ##############################################

    def __init__(self, letter, count):

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

    def compatible(self, other):
        return isinstance(other, self.__class__) and self.letter == other.letter

####################################################################################################

class Instruction(object):

    ##############################################

    def __init__(self, name, description, opcodes):

        self.name = name
        self.description = description
        self.opcodes = opcodes

    ##############################################

    def __str__(self):
        return self.name

    ##############################################

    def _parse_nibble(self, nibble):

        chuncks = []
        chunck = nibble[0]
        for c in nibble[1:]:
            if ((c in ('0', '1') and chunck[-1] in ('0', '1'))
                or chunck[-1] == c):
                chunck += c
            else:
                chuncks.append(chunck)
                chunck = c
        chuncks.append(chunck)

        # chuncks2 = []
        # for chunck in chuncks:
        #     if chunck[0] in ('0', '1'):
        #         number = sum([int(c) << i for i, c in enumerate(reversed(chunck))])
        #         chuncks2.append((number, len(chunck)))
        #     else:
        #         chuncks2.append((chunck[0], len(chunck)))

        return chuncks

    ##############################################

    def _parse_opcode(self, opcode):

        nibbles = opcode.split(' ')
        opcode_size = len(nibbles)
        opcode_string = ''.join(nibbles)
        print(opcode_string)

        # chuncks = []
        # for nibble_weight, nibble in enumerate(nibbles):
        #     for chunck in self._parse_nibble(nibble):
        #         if chuncks and chuncks[-1][0] == item:
        #             chuncks[-1][1] += count
        #         if chuncks and chuncks[-1][0] == item:
        #             chuncks[-1][1] += count
        #         else:
        #             chuncks.append([item, len()])


                # if chuncks and isinstance(item, str) and chuncks[-1][0] == item:
                #     chuncks[-1][1] += count
                # elif chuncks and isinstance(item, int) and chuncks[-1][0] == item:
                #     chuncks[-1][1] += count
                # else:
                #     chuncks.append([item, count])

        # print(chuncks)
        # if opcode_size == 4:
        #     value = 0
        #     mask = 0
        #     shift = 16
        #     operand = ''
        #     for item, count in chuncks:
        #         shift -= count
        #         if isinstance(item, int):
        #             # print(item, count, shift)
        #             value += item << shift
        #             mask += (2**(count) -1) << shift
        #             operand += '_{}'.format(item, count)
        #         else:
        #             operand += '{}{}'.format(item, count)
        #     print(hex(value), hex(mask), operand)

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
    print(instruction)
    for opcode in instruction.opcodes:
        print(opcode)
        instruction._parse_opcode(opcode)
