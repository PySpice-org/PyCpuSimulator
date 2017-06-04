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

"""Read Intel HEX file format

See Hexadecimal Object File Format Specification.
See https://en.wikipedia.org/wiki/Intel_HEX
"""

####################################################################################################

import logging

import numpy as np

####################################################################################################

from PyCpuSimulator.Math.Interval import IntervalInt

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Chunk:

    ##############################################

    def __init__(self, address, data):

        self._address = address
        self._data = data

    ##############################################

    @property
    def address(self):
        return self._address

    @property
    def interval(self):
        return IntervalInt(self._address, self._address + len(self._data) // 2)

    @property
    def data(self):
        return self._data

    @property
    def byte_array(self):
        byte_array = [int(self._data[i:i+2], 16) for i in range(0, len(self._data), 2)]
        return np.array(byte_array, dtype=np.uint8)

    ##############################################

    def append(self, data):

        self._data += data

####################################################################################################

class Chunks(list):

    ##############################################

    @property
    def interval(self):

        # Compute address range

        interval = None
        if self:
            interval = self[0].interval
            for chunk in self[1:]:
                interval |= chunk.interval
        return interval

####################################################################################################

class HexFile:

    _logger = _module_logger.getChild('Hex')

    # __start_code_size__ = 1 # 0
    # __byte_count_size__ = 2 # 1-2
    # __address_size___ = 4 # 3-6
    # __record_type_size__ = 2 # 7-8

    ##############################################

    def __init__(self, path):

        self._path = path

        # Read HEX file
        chunks = Chunks()
        next_address = None
        for line_type, address, data_size, data in self._read_hex():
            if line_type == 0:
                if next_address is None or address != next_address:
                    chunks.append(Chunk(address, data))
                else: # contiguous addressing, append data to the last chunk
                    chunks[-1].append(data)
                next_address = address + data_size
            elif line_type >= 2:
                raise NotImplementedError('Unsupported Intel 80x86 line type')
            # else: 1 is end of file

        interval = chunks.interval
        self._logger.info("Hex file {} requires {:1} kB", path, interval.sup / 1024)

        # Copy chunks to a flat memory
        self._data = np.zeros(interval.sup, dtype=np.uint8)
        for chunk in chunks:
            data = chunk.byte_array
            self._data[chunk.address:data.shape[0]] = data

    ##############################################

    def _read_hex(self):

        with open(self._path) as f:
            for line in f:
                line = line.strip()
                if not line.startswith(':'):
                    # or not line.endswith('\n')
                    raise NameError("Bad line format")
                if not self._check_checksum(line):
                    raise NameError("Bad line checksum")
                data_size = int(line[1:3], 16)
                address = int(line[3:7], 16)
                line_type = int(line[7:9], 16)
                data = line[9:-2]
                if len(data) != 2 * data_size:
                    raise NameError("Bad line size")
                yield line_type, address, data_size, data

    ##############################################

    @staticmethod
    def _check_checksum(line):

        # Checksum is the two's complement of the sum of the bytes from the byte count to the end of
        # data using uint8 arithmetic.
        return (sum([int(line[i:i+2], 16)
                    for i in range(1, len(line), 2)])
                % 256 == 0)

    ##############################################

    @property
    def data(self):
        return self._data

    ##############################################

    def __len__(self):
        return self._data.shape[0]

    ##############################################

    def uint16_length(self):
        return len(self) // 2

    ##############################################

    def read_uint16(self, i):

        return (self._data[i+1] << 8) + self._data[i]

    ##############################################

    def iter_on_uint16(self):

        for i in range(0, len(self), 2):
            yield self.read_uint16(i)
