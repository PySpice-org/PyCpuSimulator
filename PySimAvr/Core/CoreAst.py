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

def two_complement(x, number_of_bits):
    return 2**number_of_bits -1 - x

def xor(x, y, number_of_bits):
    """ x.not(y) + not(x).y  """
    return x & two_complement(y, number_of_bits) | two_complement(x, number_of_bits) & y

####################################################################################################

class Program(object):

    _logger = _module_logger.getChild('Program')

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

    def eval(self, cpu):

        for statement in self:
            statement.eval(cpu)

    ##############################################

    def __str__(self):

        return '\n'.join([str(statement) for statement in self])
    
####################################################################################################

class Assignation(object):

    ##############################################

    def __init__(self, destination, value):

        self._destination = destination
        self._value = value

    ##############################################

    def eval(self, cpu):

        self._destination.set(cpu, self._value.eval(cpu))

    ##############################################

    def __str__(self):

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
    
    ##############################################

    @property
    def operand_size(self):
        return self._operand_size
    
    ##############################################

    def eval_operands(self, cpu):
        return [operand.eval(cpu) for operand in self._operands]
    
    ##############################################

    def eval(self, cpu):

        raise NotImplementedError

####################################################################################################

class Operand(object):

    ##############################################

    def __init__(self, name):
    
        self._name = name

    ##############################################
        
    def eval(self, cpu):

        raise NotImplementedError

####################################################################################################
    
class RegisterOperand(Operand):
    def __str__(self):
        return '@' + self._name

class ConstantOperand(Operand):
    def __str__(self):
        return '$' + self._name

####################################################################################################

class Constant(object):

    ##############################################

    def __init__(self, value):
    
        self._value = value

    ##############################################
        
    def eval(self, cpu):

        return self._value

    ##############################################

    def __str__(self):
        return hex(self._value)
    
####################################################################################################

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

    ##############################################

    def __init__(self, operand, memory):
    
        super(Addressing, self).__init__(operand)
        self._memory = memory

    ##############################################

    def _memory_address(self, cpu):

        address = self.eval_operands(cpu)
        memory = cpu.memory[self._memory]
        return memory, address
    
    ##############################################

    def eval(self, cpu):
        memory, address = self._memory_address(cpu)
        return memory[address]

    ##############################################

    def set(self, cpu, value):
        memory, address = self._memory_address(cpu)
        memory[address] = value # .set(value)

    ##############################################

    def __str__(self):
        return "{}[{}]".format(self._memory, str(self.operand))
        
####################################################################################################

class Concatenation(BinaryOperator):
    __operator__ = ':'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 << self.operand_size + int(operand2)
    
####################################################################################################

class Bit(BinaryExpression):
    def __str__(self):
        return "{}[{}]".format(self.operand1, self.operand2)
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return (operand1 >> operand2) & 0x1
    
class BitRange(TernaryExpression):
    def __str__(self):
        return "{}[{}..{}]".format(str(self.operand1), str(self.operand2), str(self.operand3))
    def eval(self, cpu):
        operand1, operand2, operand3 = self.eval_operands(cpu)
        return (operand1 >> operand2) & (2**(operand3 - operand2 +1) -1)
    
class LowerNibble(TernaryExpression):
    def __str__(self):
        return str(self.operand) + "[3:0]"
    def eval(self, cpu):
        operand1 = self.eval_operands(cpu)
        return operand1 & 0x0F

class UpperNibble(TernaryExpression):
    def __str__(self):
        return str(self.operand) + "op1[7:4]"
    def eval(self, cpu):
        operand1 = self.eval_operands(cpu)
        return operand1 >> 4
    
####################################################################################################

class Addition(BinaryOperator):
    __operator__ = '+'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 + operand2

class Subtraction(BinaryOperator):
    __operator__ = '-'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 - operand2

class Multiplication(BinaryOperator):
    __operator__ = '*'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 * operand2

class Division(BinaryOperator):
    __operator__ = '/'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 // operand2

####################################################################################################

class And(BinaryOperator):
    __operator__ = '&'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 & operand2

class Or(BinaryOperator):
    __operator__ = '|'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 | operand2

class Xor(BinaryOperator):
    __operator__ = '|!'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return xor(operand1, operand2, self.operand_size)

class LeftShift(BinaryOperator):
    __operator__ = '<<'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 << operand2

class RightShift(BinaryOperator):
    __operator__ = '>>'
    def eval(self, cpu):
        operand1, operand2 = self.eval_operands(cpu)
        return operand1 >> operand2

####################################################################################################
# 
# End
# 
####################################################################################################
