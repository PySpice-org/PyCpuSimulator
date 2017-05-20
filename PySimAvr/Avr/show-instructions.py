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

####################################################################################################

from Instruction import instructions, DecisionTree

####################################################################################################

# opcode = instructions['DEC'].first_opcode
# opcode.opcode_intervals()

# bytecode_interval_pool = []
# for instruction in instructions.values():
#     for opcode in instruction.opcodes:
#         bytecode_intervals = opcode.opcode_intervals()
#         print(instruction.mnemonic, opcode.opcode_string, ' '.join([str(x) for x in bytecode_intervals]))
#         for interval in bytecode_intervals:
#             bytecode_interval_pool.append((interval, opcode))
# for interval1, opcode1 in bytecode_interval_pool:
#     for interval2, opcode2 in bytecode_interval_pool:
#         if interval1 is not interval2:
#             if interval1.intersect(interval2):
#                 print("{} {} {} and {} {} {} clash".format(opcode1.mnemonic, opcode1, str(interval1),
#                                                            opcode2.mnemonic, opcode2, str(interval2)))
        
# for instruction in instructions.values():
#     print()
#     print(instruction.mnemonic)
#     for i, opcode in enumerate(instruction.opcodes):
#         print(i, opcode.operation)

for instruction in instructions.values():
    for i, opcode in enumerate(instruction.opcodes):
        if opcode.operation is not None and '<-' in opcode.operation:
            print(opcode.operation)

# for instruction in instructions.values():
#     print()
#     print(instruction.mnemonic)
#     for i, opcode in enumerate(instruction.opcodes):
#         print("  {:2} 0x{:04x} 0x{:04x} | {} | {} | {}".format(
#             i,
#             opcode.opcode, opcode.mask,
#             opcode.opcode_string,
#             opcode.operand_pattern,
#             ' '.join(opcode.opcode_operands),
#         ))

# sbc = instructions['SBC'].first_opcode
# print(sbc.instruction.mnemonic, sbc.opcode_string)
# operands_in = dict(r=15, d=31)
# bytecode = sbc.encode(**operands_in)
# operands_out = sbc.decode(bytecode)
# print(operands_in, bin(bytecode), operands_out)

# ldd = instructions['LDD'].first_opcode
# print(ldd.instruction.mnemonic, ldd.opcode_string)
# operands_in = dict(d=0xA, q=0x2A)
# bytecode = ldd.encode(**operands_in)
# operands_out = ldd.decode(bytecode)
# print(operands_in, bin(bytecode), operands_out)

# print("\nMulti-Opcodes Instructions:")
# for instruction in instructions.values():
#     if not instruction.single_opcode:
#         print(' ', instruction.mnemonic)

# print("\n32-bit Opcodes:")
# for instruction in instructions.values():
#     for opcode in instruction.opcodes:
#         if opcode.opcode_size == 32:
#             print('  {:6s} 0x{:04x} 0x{:04x}'.format(instruction.mnemonic, opcode.opcode, opcode.mask))
        
# print("\nOpcodes without operand:")
# for instruction in instructions.values():
#     # if instruction.no_operand:
#     for opcode in instruction.opcodes:
#         if opcode.no_operand:
#             print('  {:6s} 0x{:04x}'.format(instruction.mnemonic, opcode.opcode))
            
# print("\nOperand patterns:")
# operand_patterns = {}
# for instruction in instructions.values():
#     for opcode in instruction.opcodes:
#         if opcode.no_operand:
#             continue
#         if opcode.operand_pattern in operand_patterns:
#             operand_patterns[opcode.operand_pattern] += 1
#         else:
#             operand_patterns[opcode.operand_pattern] = 1
# for operand_pattern in sorted(operand_patterns):
#     print('  {:16} {:3}'.format(operand_pattern, operand_patterns[operand_pattern]))

# print("\nOpcodes:")
# opcodes = []
# for instruction in instructions.values():
#     for opcode in instruction.opcodes:
#         opcodes.append(opcode)
# for opcode in sorted(opcodes, key=lambda x: x.opcode):
#     print('  0x{:04x} 0x{:04x} {}'.format(opcode.opcode, opcode.mask, opcode.instruction.mnemonic))

# decision_tree = DecisionTree(instructions)
# print("\nMasks:")
# decision_tree.print_masks()
# print("\nDecision Tree:")
# decision_tree.print_tree()

####################################################################################################
# 
# End
# 
####################################################################################################
