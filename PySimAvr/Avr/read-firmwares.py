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

from PySimAvr.Avr.Instruction import instructions, DecisionTree
from PySimAvr.BinaryFormat.HexFile import HexFile

####################################################################################################

# path = '/home/gv/sys/fc14/fabrice/Arduino/blink-led/.build/mega2560/firmware.hex'
# hex_file = HexFile(path)

# for i in range(0, 16, 2):
#     print("0x{:04X}".format((hex_file.data[i+1] << 8) + hex_file.data[i]))

####################################################################################################

# for each opcode fill table[2**16] bytecode -> opcode, operands
# use it to check dt

decision_tree = DecisionTree(instructions)
print("\nDecision Tree:")
decision_tree.print_tree()

  #  0:	0c 94 26 01 	jmp	0x24c	; 0x24c <__ctors_end>
  # e4:	76 02       	muls	r23, r22

# opcode = instructions['JMP'].first_opcode
# print("opcode mask Ox{:04x}".format(opcode.mask))
  
# decision_tree.find_instruction(int('940c', 16))
  
####################################################################################################
# 
# End
# 
####################################################################################################
