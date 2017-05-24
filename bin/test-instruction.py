#! /usr/bin/env python3

####################################################################################################
#
# PySimAvr - AVR Simulator
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

"""Test the bytecode decoder.
"""

####################################################################################################

from PySimAvr.Avr import instruction_set

from PySimAvr.Tools.BinaryNumber import sup_for_nbits, format_as_nibble

####################################################################################################
#
# Check Instruction Set
#

# check the instruction set for bytecode clash
instruction_set.check_for_clash(verbose=False)

# Build and verify the decision tree
decision_tree = instruction_set.decision_tree
decision_tree.brut_force_check()
if True:
    decision_tree.print()

####################################################################################################
#
# Encode / Decode Instruction
#

if True:
    sbc = instruction_set['SBC'].first_opcode
    print(sbc.instruction.mnemonic, sbc.opcode_string)
    operands_in = dict(r=15, d=31)
    bytecode = sbc.encode(**operands_in)
    operands_out = sbc.decode(bytecode)
    print(operands_in, '->', bin(bytecode), '->', operands_out)

    ldd = instruction_set['LDD'].first_opcode
    print(ldd.instruction.mnemonic, ldd.opcode_string)
    operands_in = dict(d=0xA, q=0x2A)
    bytecode = ldd.encode(**operands_in)
    operands_out = ldd.decode(bytecode)
    print(operands_in, '->', bin(bytecode), '->', operands_out)

####################################################################################################

# Dump all the bytecodes for an opcode
if True:
    opcode = instruction_set['LDD'].first_opcode
    print(opcode.opcode_string)
    for bytecode in opcode.iter_on_bytecodes():
        print(format_as_nibble(bytecode))

####################################################################################################

# Dump instruction set properties
if True:
    print("\nMulti-Opcodes Instructions:")
    for instruction in instruction_set.iter_on_instructions():
        if not instruction.single_opcode:
            print(' ', instruction.mnemonic)

    print("\n32-bit Opcodes:")
    for instruction in instruction_set.iter_on_instructions():
        for opcode in instruction.opcodes:
            if opcode.opcode_size == 32:
                print('  {:6s} 0x{:04x} 0x{:04x}'.format(instruction.mnemonic, opcode.opcode, opcode.mask))

    print("\nOpcodes without operand:")
    for instruction in instruction_set.iter_on_instructions():
        # if instruction.no_operand:
        for opcode in instruction.opcodes:
            if opcode.no_operand:
                print('  {:6s} 0x{:04x}'.format(instruction.mnemonic, opcode.opcode))

    print("\nOperand patterns:")
    operand_patterns = {}
    for instruction in instruction_set.iter_on_instructions():
        for opcode in instruction.opcodes:
            if opcode.no_operand:
                continue
            if opcode.operand_pattern in operand_patterns:
                operand_patterns[opcode.operand_pattern] += 1
            else:
                operand_patterns[opcode.operand_pattern] = 1
    for operand_pattern in sorted(operand_patterns):
        print('  {:16} {:3}'.format(operand_pattern, operand_patterns[operand_pattern]))

####################################################################################################

# Dump operations
if True:
    for instruction in instruction_set.iter_on_instructions():
        print()
        print(instruction.mnemonic)
        for i, opcode in enumerate(instruction.opcodes):
            print(i, opcode.operation)

# Dump opcodes
if True:
    for instruction in instruction_set.iter_on_instructions():
        print()
        print(instruction.mnemonic)
        for i, opcode in enumerate(instruction.opcodes):
            print("  {:2} 0x{:04x} 0x{:04x} | {} | {} | {}".format(
                i,
                opcode.opcode, opcode.mask,
                opcode.opcode_string,
                opcode.operand_pattern,
                ' '.join(opcode.opcode_operands),
            ))

if True:
    print("\nOpcodes:")
    opcode_set = instruction_set.opcode_set()
    for opcode in sorted(opcode_set, key=lambda x: x.opcode):
        print('  0x{:04x} 0x{:04x} {}'.format(opcode.opcode, opcode.mask, opcode.instruction.mnemonic))

####################################################################################################
#
# Bytecode Interval (but code is wrong)
#

# Fixme: what means (but code is wrong) ???

if True:
    bytecode_interval_pool = []
    for instruction in instruction_set.iter_on_instructions():
        for opcode in instruction.opcodes:
            try:
                bytecode_intervals = opcode.opcode_intervals()
                print(instruction.mnemonic, opcode.opcode_string, ' '.join([str(x) for x in bytecode_intervals]))
                for interval in bytecode_intervals:
                    bytecode_interval_pool.append((interval, opcode))
            except NotImplementedError:
                pass
    for interval1, opcode1 in bytecode_interval_pool:
        for interval2, opcode2 in bytecode_interval_pool:
            if interval1 is not interval2:
                if interval1.intersect(interval2):
                    print("{} {} {} and {} {} {} clash".format(opcode1.mnemonic, opcode1, str(interval1),
                                                               opcode2.mnemonic, opcode2, str(interval2)))
