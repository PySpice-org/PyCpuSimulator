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

from PySimAvr.Avr import instruction_set
from PySimAvr.BinaryFormat.HexFile import HexFile
from PySimAvr.Core.Instruction import DecodeError

####################################################################################################

path = '/home/gv/sys/fc14/fabrice/Arduino/blink-led/.build/mega2560/firmware.hex'
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

# avr-objdump -D --prefix-addresses firmware.elf

####################################################################################################
#
# End
#
####################################################################################################
