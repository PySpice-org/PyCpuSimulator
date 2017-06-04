####################################################################################################
#
# PySimAvr - AVR Simulator
# Copyright (C) 2017 Fabrice Salvaire
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

"""Parse binutils objdump output.
"""

####################################################################################################

import subprocess
import logging

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ParseError(Exception):

    ##############################################

    def __init__(self, line_number):

        self._line_number = line_number

####################################################################################################

class ObjDumpLine:

    ##############################################

    def __init__(self, address, instruction_bytes, instruction, comment):

        self._address = address
        self._instruction_bytes = instruction_bytes
        self._mnemonic = instruction[0].upper()
        self._operands = instruction[1] if len(instruction) == 2 else None
        self._comment = comment

    ##############################################

    @property
    def address(self):
        return self._address

    @property
    def instruction_bytes(self):
        return self._instruction_bytes

    @property
    def mnemonic(self):
        return self._mnemonic

    @property
    def operands(self):
        return self._operands

    @property
    def comment(self):
        return self._comment

    @property
    def is_word(self):
        return self._mnemonic == '.word'

    ##############################################

    def __repr__(self):

        return '{0.address:X}: {0.instruction_bytes} | {0.mnemonic} {0.operands} | {0.comment}'.format(self)

####################################################################################################

class ObjDump:

    ##############################################

    def __init__(self, hex_path, machine='avr6'):

        self._hex_path = hex_path

        self._lines = []
        self._map = []

        output = self._run_objdump(hex_path, machine)
        self._parse_output(output)
        self._make_map()

    ##############################################

    def _run_objdump(self, hex_path, machine):

        self._section = '.sec1'
        command = ('avr-objdump',
                   '--disassemble',
                   '--section={}'.format(self._section),
                   '--architecture={}'.format(machine),
                   hex_path
        )
        output = subprocess.check_output(command)

        return output.decode('ascii')

    ##############################################

    def _parse_output(self, output):

        #
        # blink-led-mega2560-firmware.hex:     file format ihex
        #
        #
        # Disassembly of section .sec1:
        #
        # 00000000 <.sec1>:
        #    0:	0c 94 26 01 	jmp	0x24c	;  0x24c

        read_hex_path = True
        read_section = True
        read_section_address = True

        for line_number, line in enumerate(output.split('\n')):
            line = line.strip()
            if not line:
                continue
            if read_hex_path and line.startswith(self._hex_path + ':'): #  + ':     file format ihex'
                read_hex_path = False
            elif read_section and line == 'Disassembly of section {}:'.format(self._section):
                read_section = False
            elif read_section_address and '<{}>'.format(self._section) in line:
                read_section_address = True
            elif line == '...':
                pass
            else: # dump
                # print('> ' + line)
                address_position = line.find(':')
                comment_position = line.find(';')
                if address_position == -1:
                    raise ParseError(line_number)
                address = int(line[:address_position], base=16)
                start = address_position +1
                if comment_position == -1:
                    middle = line[start:]
                    comment = ''
                else:
                    middle = line[start:comment_position]
                    comment = line[comment_position +1:].strip()
                middle = middle.strip()
                parts = [x.strip() for x in middle.split('\t')]
                instruction_bytes, instruction = parts[0], parts[1:]
                objdump_line = ObjDumpLine(address, instruction_bytes, instruction, comment)
                # print(objdump_line)
                self._lines.append(objdump_line)

    ##############################################

    def _make_map(self):

        last_address = self._lines[-1].address
        self._map = [None] * (last_address + 1)

        for line in self._lines:
            self._map[line.address] = line

    ##############################################

    def __iter__(self):

        return iter(self._lines)

    ##############################################

    def __getitem__(self, address):

        return self._map[address]

