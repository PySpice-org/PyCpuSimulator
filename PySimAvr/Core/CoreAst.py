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

import logging

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Program(object):

    ##############################################

    def __init__(self):

        self._statements = []

    ##############################################

    def __iter__(self):

        return iter(self._statements)
        
    ##############################################

    def add(self, statement):

        # Fixme: reverse ?
        # self._statements.append(statement)
        self._statements.insert(0, statement)

    ##############################################

    def __str__(self):

        return '\n'.join([str(statement) for statement in self])
    
####################################################################################################

class Operand(object):
    def __init__(self, name):
        self._name = name

class RegisterOperand(Operand):
    def __str__(self):
        return '@' + self._name

class ConstantOperand(Operand):
    def __str__(self):
        return '$' + self._name

####################################################################################################

class Register(object):
    def __init__(self, name):
        self._name = name
        
    def __str__(self):
        return self._name
    
####################################################################################################

class Constant(object):
    def __init__(self, value):
        self._value = value

    def __int__(self):
        return self._value
        
    def __str__(self):
        return hex(self._value)
    
####################################################################################################

class Assignation(object):
    def __init__(self, destination, value):
        self._destination = destination
        self._value = value

    @property
    def destination(self):
        return self._destination

    @property
    def value(self):
        return self._value
    
    def __str__(self):
        # ←
        return ' '.join((str(self._destination), '<-', str(self._value)))
    
####################################################################################################

class Expression(object):

    __number_of_operands__ = None
    
    ##############################################

    def __init__(self, *args, **kwargs):

        if len(args) != self.__number_of_operands__:
            raise ValueError("Wrong number of operands")
        
        self._operands = args
        # self._operand_size = args[0].size
        # for operand in self._operands[1:]:
        #     if operand.size != self._operand_size:
        #         raise ValueError('Incompatible operands')

    ##############################################

    def iter_on_operands(self):
        return iter(self._operands)
    
    ##############################################

    @property
    def operand(self):
        return self._operands[0]
    
    @property
    def operand1(self):
        return self._operands[0]

    @property
    def operand2(self):
        return self._operands[1]

    @property
    def operand3(self):
        return self._operands[2]

class UnaryExpression(Expression):
    __number_of_operands__ = 1
    
class BinaryExpression(Expression):
    __number_of_operands__ = 2
    
class TernaryExpression(Expression):
    __number_of_operands__ = 3

####################################################################################################

class BinaryOperator(BinaryExpression):
    __operator__ = None

    def __str__(self):
        return ' '.join((str(self.operand1), self.__operator__, str(self.operand2)))

####################################################################################################

class Addressing(UnaryExpression):
    def __init__(self, memory, address):
        super(Addressing, self).__init__(address)
        self._memory = memory
    
    @property
    def memory(self):
        return self._memory
        
    def __str__(self):
        return "{}[{}]".format(self._memory, str(self.operand))
        
####################################################################################################

class Concatenation(BinaryOperator):
    __operator__ = ':'

class Bit(BinaryExpression):
    def __str__(self):
        return "{}[{}]".format(self.operand1, self.operand2)
    
class BitRange(TernaryExpression):
    def __str__(self):
        return "{}[{}..{}]".format(str(self.operand1), str(self.operand2), str(self.operand3))
    
class LowerNibble(TernaryExpression):
    def __str__(self):
        return str(self.operand) + "[3:0]"

class UpperNibble(TernaryExpression):
    def __str__(self):
        return str(self.operand) + "op1[7:4]"
    
####################################################################################################

class Addition(BinaryOperator):
    __operator__ = '+'

class Subtraction(BinaryOperator):
    __operator__ = '-'

class Multiplication(BinaryOperator):
    __operator__ = '*'

class Division(BinaryOperator):
    __operator__ = '/'

####################################################################################################

class And(BinaryOperator):
    __operator__ = '&'

class Or(BinaryOperator):
    __operator__ = '|'

class Xor(BinaryOperator):
    __operator__ = '|!'

class LeftShift(BinaryOperator):
    __operator__ = '<<'

class RightShift(BinaryOperator):
    __operator__ = '>>'

####################################################################################################
# 
# End
# 
####################################################################################################
