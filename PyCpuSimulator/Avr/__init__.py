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

"""Load AVR Instruction Set from YAML file.
"""

# Fixme:
# and: & ∧ •
#  or: | ∨ +
# xor: ^ ⊻ ⊗
# not: ! ¬

####################################################################################################

__all__ = ['instruction_set']

####################################################################################################

import os as _os

####################################################################################################

from PyCpuSimulator.Core.Instruction import InstructionSet

####################################################################################################

_yaml_path = _os.path.join(_os.path.dirname(__file__), 'opcodes.yml')

#: Dictionnary providing the :class:`Instruction` instances for the AVR instruction set.
instruction_set = InstructionSet(_yaml_path)
