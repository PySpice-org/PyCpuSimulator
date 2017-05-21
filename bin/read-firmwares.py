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

"""Read a firmware in Intel HEX format and dump disassembled instructions.

How to disassemble using GNU Binutils::

  avr-objdump -D --prefix-addresses firmware.elf
  avr-objdump -d -j .sec1 -m avr6 firmware.hex
"""

####################################################################################################

# Fixme: End of program issue
#
# 0x066E: 0xCFFF
#    RJMP 1100 kkkk kkkk kkkk
#   {'k': 4095}
# 0x0670: 0x000D
#   Illegal instruction
#
# objdump output is:
#
# 66a:	f8 94       	cli
# 66c:	ff cf       	rjmp	.-2      	;  0x66c
# 66e:	0d 00       	.word	0x000d	; ????

# Fixme: What is this word ???

####################################################################################################

from PySimAvr.Avr import instruction_set
from PySimAvr.BinaryFormat.HexFile import HexFile
from PySimAvr.Core.Instruction import DecodeError

####################################################################################################

# Fixme: use argparse ...
path = 'data/blink-led-mega2560-firmware.hex'

####################################################################################################

hex_file = HexFile(path)

decision_tree = instruction_set.decision_tree

bytecode_iterator = hex_file.iter_on_uint16()
pc = 0
pc_stop = len(hex_file)
while pc < pc_stop:
    bytecode = next(bytecode_iterator)
    pc += 2
    print('0x{:04X}: 0x{:04X}'.format(pc, bytecode))
    try:
        opcode = decision_tree.decode(bytecode)
        print('  ', opcode.mnemonic, opcode)
        if opcode.opcode_size == 32:
            operand_bytecode = next(bytecode_iterator)
            print('0x{:04X}: 0x{:04X}'.format(pc +2, operand_bytecode))
            pc += 2
        else:
            print(' ', opcode.decode(bytecode))
    except DecodeError:
        print("  Illegal instruction")
