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

__all__ = ['sup_for_nbits', 'format_as_nibble']

####################################################################################################

import ansicolor

####################################################################################################

def sup_for_nbits(n):
    return 2**n -1

####################################################################################################

_hex_to_bin =  {hex(x)[2:]:"{:04b}".format(x) for x in range(16)}

def format_as_nibble(x):
    return ' '.join([_hex_to_bin[x] for x in hex(x)[2:]])

####################################################################################################

def format_and_colour_with_mask(value, mask, number_of_bits, colour=ansicolor.red):
    string = ''
    for i in range(number_of_bits -1, -1, -1):
        bit = '1' if (value >> i) & 1 else '0'
        if (mask >> i) & 1:
            string += colour(bit)
        else:
            string += bit
    return string
