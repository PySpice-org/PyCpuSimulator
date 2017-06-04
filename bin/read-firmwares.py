#! /usr/bin/env python3

####################################################################################################
#
# PyCpuSimulator - AVR Simulator
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

from PyCpuSimulator.Avr.HexFile import HexFile, HexOpcode

####################################################################################################

# Fixme: use argparse ...
path = 'data/blink-led-mega2560-firmware.hex'

####################################################################################################

hex_file = HexFile(path)

for hex_opcode in hex_file.read_opcodes():
    if isinstance(hex_opcode, HexOpcode):
        template = '0x{0.address:04X}: 0x{0.bytecode:04X}\n  {0.opcode.mnemonic} {0.opcode}'
        print(template.format(hex_opcode))
        if hex_opcode.opcode_size == 32:
            print('0x{:04X}: 0x{:04X}'.format(hex_opcode.address +2, hex_opcode.operand_bytecode))
        else:
            print(' ', hex_opcode.decode())
    else:
        template = '0x{0.address:04X}: 0x{0.bytecode:04X}\n  word ???'
        print(template.format(hex_opcode))
