####################################################################################################
#
# PyCpuSimulator - .
# Copyright (C) 2015 Salvaire Fabrice
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

import os

####################################################################################################

class BitRegister(object):

    ##############################################

    def __init__(self, byte_register, bit, name):

        self.byte_register = byte_register
        self.bit = bit
        self.name = name

    ##############################################

    def __repr__(self):
        return '{} 0x{:03x}({})'.format(self.name, self.byte_register.address, bit)

####################################################################################################

class ByteRegister(object):

    ##############################################

    def __init__(self, address, name, bits=None):

        self.address = address
        self.name = name

        if bits is not None:
            self.bits = [BitRegister(self, i, name)
                         for i, name in enumerate(bits)
                         if name]
        else:
            self.bits = None

    ##############################################

    def __repr__(self):
        return '{} 0x{:03x}(0:7)'.format(self.name, self.address)

####################################################################################################

class NibbleRegister(ByteRegister):

    ##############################################

    def __repr__(self):
        return '{} 0x{:03x}(0:3)'.format(self.name, self.address)

####################################################################################################

_csv_name = 'atmega-640-1280-2560.register-summary.csv'
_csv_path = os.path.join(os.path.dirname(__file__), _csv_name)

number_of_registers = 0x200
sram = [None]*number_of_registers

with open(_csv_path) as f:
    for line in f:
        line = line.strip()
        bits = [None]*8
        (address, name,
         bits[7], bits[6], bits[5], bits[4], bits[3], bits[2], bits[1], bits[0],
         page) = line.split('|')
        if address in ('Address', '...') or name == 'Reserved':
            continue
        address = int(address, 16)
        bit_pattern = ''
        for i in range(8):
            if not bits[i]:
                bit_pattern += '>'
            elif bits[i] == '-':
                bit_pattern += '-'
                bits[i] = None # unused
            else:
                bit_pattern += 'b'
        if bit_pattern == '>>>b----':
            register = NibbleRegister(address, name)
        elif bit_pattern == '>>>>>>>b':
            register = ByteRegister(address, name)
        elif '>' not in bit_pattern:
            register = ByteRegister(address, name, bits)
        else:
            raise ValueError(line)
        sram[address] = register

for address in range(number_of_registers):
    print(sram[address])
