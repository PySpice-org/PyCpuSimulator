#! /usr/bin/env python

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

# Fixme:
# Assignation RAM[REGISTER[X]] <- REGISTER[R2]
#   Addressing REGISTER[R2]
#     Register R2
#       = R2
#     = R2
#   Addressing RAM[REGISTER[X]]
#     Addressing REGISTER[X]
#       Register X
#         = X
#       = X
#     = RAM[0x3]
# Traceback (most recent call last):
#   File "bin/test-core.py", line 86, in <module>
#     core.run_ast_program(ast_program)
#   File "/home/fabrice/home/developpement/PySimAvr/PySimAvr/Core/Core.py", line 451, in run_ast_program
#     self.eval_statement(0, statement)
#   File "/home/fabrice/home/developpement/PySimAvr/PySimAvr/Core/Core.py", line 432, in eval_statement
#     value = evaluator(level, statement, *args)
#   File "/home/fabrice/home/developpement/PySimAvr/PySimAvr/Core/Core.py", line 504, in eval_Assignation
#     cell.set(value)
#   File "/home/fabrice/home/developpement/PySimAvr/PySimAvr/Core/Core.py", line 287, in set
#     self._memory[self._address] = value
#   File "/home/fabrice/home/developpement/PySimAvr/PySimAvr/Core/Core.py", line 344, in __setitem__
#     self._memory[address_slice] = value
# IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices

####################################################################################################
#
# Logging
#

import PySimAvr.Logging.Logging as Logging

logger = Logging.setup_logging('pysimavr')

####################################################################################################

from PySimAvr.Core.CoreHdlParser import Parser
from PySimAvr.Core.Core import (StandardCore,
                                RegisterFile, RamMemory,
                                MappedRegister, Register8, Register16)

####################################################################################################

micro_code_parser = Parser()

ram = RamMemory('RAM', cell_size=8, size=8*1024)

general_purpose_registers = [Register8('R' + str(i)) for i in range(4)]
registers = [
    Register16('PC'),
    Register16('STACK'),
    Register8('SREG'),
    Register16('X'),
    MappedRegister('Y', ram.cell(0)),
]
registers.extend(general_purpose_registers)

register_file = RegisterFile('REGISTER', registers)

core = StandardCore(memories=(register_file, ram))

####################################################################################################

print()

source = '''
R0 = 10 + 10;
R1 = 20;
R2 = R0 + R1;
R2 = R2 ^ R2;
R2 = R0 + 30;
X = 0x3;
[X] = R2;
R1 = 1;
if (R1 == 1) {
  R2 = 3;
  [0x4] = 0x1F;
}
else
  R2 = 4;
Y = 23;
'''


rule = '\n' + '-'*100 + '\n'

print(source)

# micro_code_parser.test_lexer(source)

ast_program = micro_code_parser.parse(source)

# print()
# print(ast_program)

print(rule)
core.run_ast_program(ast_program)

print(ram[:10])
