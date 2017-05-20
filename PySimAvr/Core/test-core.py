#! /usr/bin/env python

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
#
# Logging
#

import PySimAvr.Logging.Logging as Logging

logger = Logging.setup_logging('pysimavr')

####################################################################################################

from PySimAvr.Core.CoreHdlParser import Parser
from PySimAvr.Core.Core import (StandardCore,
                                RegisterMemory, RamMemory,
                                Register8, Register16)

####################################################################################################

micro_code_parser = Parser()

general_purpose_registers = [Register8('R' + str(i)) for i in range(4)]
register_definitions = [
    Register16('PC'),
    Register16('STACK'),
    Register8('SREG'),
    Register16('X'),
]
register_definitions.extend(general_purpose_registers)

ram = RamMemory('RAM', cell_size=8, size=8*1024)
registers = RegisterMemory('REGISTER', register_definitions)

core = StandardCore(memories=(registers, ram))

####################################################################################################

print()

source = '''
R0 <- 10 + 10;
R1 <- 20;
R2 <- R0 + R1;
R2 <- R2 |! R2;
R2 <- R0 + 30;
X <- 0x13;
[X] <- R2;
'''
print(source)
micro_code_parser.test_lexer(source)
ast_program = micro_code_parser.parse(source)
# print()
# print(ast_program)
print()
core.run_ast_program(ast_program)

####################################################################################################
# 
# End
# 
####################################################################################################
