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

"""Read an AVR firmware in Intel HEX format.
"""

###################################################################################################

from . import instruction_set
from PySimAvr.BinaryFormat import HexFile
from PySimAvr.Core.Instruction import DecodeError

####################################################################################################

class HexWord:

    ##############################################

    def __init__(self, address, bytecode):

        self._address = address
        self._bytecode = bytecode

    ##############################################

    @property
    def address(self):
        return self._address

    @property
    def bytecode(self):
        return self._bytecode

####################################################################################################

class HexOpcode(HexWord):

    __decision_tree__ = instruction_set.decision_tree

    ##############################################

    def __init__(self, address, bytecode):

        HexWord.__init__(self, address, bytecode)
        self._opcode = self.__decision_tree__.decode(bytecode)
        self._operand_bytecode = None

    ##############################################

    @property
    def opcode(self):
        return self._opcode

    @property
    def opcode_size(self):
        return self._opcode.opcode_size

    @property
    def operand_bytecode(self):
        return self._operand_bytecode

    @operand_bytecode.setter
    def operand_bytecode(self, value):
        self._operand_bytecode = value

    ##############################################

    def decode(self):

        return self._opcode.decode(self._bytecode)

####################################################################################################

class HexFile(HexFile.HexFile):

    ##############################################

    def read_opcodes(self):

        bytecode_iterator = self.iter_on_uint16()

        address = 0
        address_stop = len(self)
        while address < address_stop:
            bytecode = next(bytecode_iterator)
            try:
                hex_opcode = HexOpcode(address, bytecode)
                if hex_opcode.opcode_size == 32:
                    hex_opcode.operand_bytecode = next(bytecode_iterator)
                    address += 2
                yield hex_opcode
            except DecodeError:
                yield HexWord(address, bytecode)
            address += 2
