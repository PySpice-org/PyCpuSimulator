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

from collections import OrderedDict
import logging

import numpy as np

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def two_complement(x, number_of_bits):
    return 2**number_of_bits -1 - x

def xor(x, y, number_of_bits):
    """ x.not(y) + not(x).y  """
    return x & two_complement(y, number_of_bits) | two_complement(x, number_of_bits) & y

####################################################################################################

class Memory(object):

    ##############################################    

    def __init__(self, name):

        self._name = name

    ##############################################

    @property
    def name(self):
        return self._name
    
####################################################################################################
        
class CellSizeMemory(Memory):

    ##############################################    

    def __init__(self, name, cell_size):

        super(CellSizeMemory, self).__init__(name)
        self._cell_size = cell_size

    ##############################################

    @property
    def cell_size(self):
        return self._cell_size
    
    ##############################################

    def np_dtype(self):
        
        if self._cell_size == 8:
            return  np.uint8
        elif self._cell_size == 16:
            return np.uint16
        elif self._cell_size == 32:
            return np.uint32
        elif self._cell_size == 64:
            return np.uint64
        else:
            raise ValueError("Wrong data size")

####################################################################################################

class Register(CellSizeMemory):

    __cell_size__ = None
    
    ##############################################    

    def __init__(self, name, cell_size=None):

        if cell_size is None:
            cell_size = self.__cell_size__
        
        super(Register, self).__init__(name, cell_size)
        
        self._dtype = self.np_dtype()
        self._value = self._dtype(0)
        
    ##############################################

    def reset(self):
        self._value = self._dtype(0)

    ##############################################

    def __int__(self):
        return int(self._value) # make a copy
        
    ##############################################

    @property
    def v(self):
        return int(self._value) # self._dtype(self._value)
        
    ##############################################

    @v.setter
    def v(self, value):
        self._value = self._dtype(value)

    ##############################################

    def __str__(self):
        return "{}: 0x{:X}".format(self._name, self._value)

class Register8(Register):
  __cell_size__ = 8

class Register16(Register):
  __cell_size__ = 16
  
class Register32(Register):
  __cell_size__ = 32

class Register64(Register):
  __cell_size__ = 64
  
####################################################################################################

class RegisterMemory(Memory):

    ##############################################    

    def __init__(self, name, registers):

        super(RegisterMemory, self).__init__(name)

        self._registers = OrderedDict([(register.name, register)
                                       for register in registers])

    ##############################################

    def reset(self):

        for register in self._registers.values():
            register.reset()
        
    ##############################################

    def __getitem__(self, register):

        return self._registers[register]

    ##############################################

    def __setitem__(self, register, value):

        self._registers[register].v = value

    ##############################################

    def dump(self):

        # for register in self._sorted_register:
        #     print(self._registers[register])
        print(' | '.join([str(self._registers[register]) for register in self._registers]))
        
####################################################################################################

class RomMemory(CellSizeMemory):

    ##############################################    

    def __init__(self, name, cell_size, size, data=None):

        super(RomMemory, self).__init__(name, cell_size)

        self._memory = np.zeros(size, dtype=self.np_dtype())
        if data is not None:
            self._memory[...] = data
    
    ##############################################

    @property
    def size(self):
        return self._memory.shape[0]
    
    ##############################################

    def __getitem__(self, address):

        return self._memory[address]
        
####################################################################################################

class RamMemory(RomMemory):

    ##############################################

    def reset(self):

        self._memory[...] = 0
    
    ##############################################

    def __setitem__(self, address, value):

        self._memory[address] = value
        
####################################################################################################

class Core(object):

    _logger = _module_logger.getChild('Core')
    
    ##############################################

    def __init__(self, memories):

        self._memories = {memory.name:memory for memory in memories}
        self._cycles = 0 # could be a register

    ##############################################

    @property
    def memory(self):
        return self._memories # Fixme:

    ##############################################

    @property
    def cycles(self):
        return self._cycles

    ##############################################

    def increment_cycle(self, cycles):
        self._cycles += cycles

    ##############################################

    def reset(self):

        self._cycles = 0
        for memory in self._memories.values():
            if hasattr(memory, 'reset'):
                memory.reset()

    ##############################################

    def eval_statement(self, statement, level=0):

        self._logger.debug('')
        
        statement_class = statement.__class__.__name__
        print('  '*level + statement_class, statement)
        evaluator = getattr(self, 'eval_' + statement_class)
        value = evaluator(statement, level)
        if value is not None:
            if isinstance(value, str):
                value_string = value
            else:
                value_string = hex(int(value))
            print('  '*level + '=', value_string)
        return value
        
    ##############################################

    def eval_operands(self, statement, level):

        self._logger.debug('')
        
        return [self.eval_statement(operand, level+1)
                for operand in statement.iter_on_operands()]
                
    ##############################################
    
    def run_ast_program(self, program):

        for statement in program:
            print()
            self.eval_statement(statement)
            self.memory['REGISTER'].dump()
            
####################################################################################################

class StandardCore(Core):

    ##############################################
    
    def eval_Assignation(self, statement, level):

        self._logger.debug('')
        
        value = self.eval_statement(statement.value, level+1)
        self.set_Addressing(statement.destination, value, level)
        
    ##############################################
        
    def eval_Constant(self, statement, level):

        return int(statement)

    ##############################################
        
    def eval_Register(self, statement, level):

        return str(statement)
    
    ##############################################

    def _memory_address(self, statement, level):

        self._logger.debug('')
        
        address = self.eval_operands(statement, level)[0]
        memory = self.memory[statement.memory]
        return memory, address
    
    ##############################################

    def eval_Addressing(self, statement, level):

        self._logger.debug('')
        
        memory, address = self._memory_address(statement, level)
        return memory[address]

    ##############################################

    def set_Addressing(self, statement, value, level):

        self._logger.debug('')
        
        memory, address = self._memory_address(statement, level)
        memory[address] = value # .set(value)
        print('  '*(level+1) + '{}[{}] <- 0x{:x}'.format(memory.name, address, value))
        
    ##############################################
        
    def eval_Concatenation(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 << statement.operand1.operand_size + int(operand2)

    ##############################################

    def eval_Bit(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return (operand1 >> operand2) & 0x1

    ##############################################
    
    def eval_BitRange(self, statement, level):

        operand1, operand2, operand3 = self.eval_operands(statement, level)
        return (operand1 >> operand2) & (2**(operand3 - operand2 +1) -1)

    ##############################################    

    def eval_LowerNibble(self, statement, level):

        operand1 = self.eval_operands(statement, level)
        return operand1 & 0x0F

    ##############################################

    def eval_UpperNibble(self, statement, level):

        operand1 = self.eval_operands(statement, level)
        return operand1 >> 4

    ##############################################
    
    def eval_Addition(self, statement, level):
        
        operand1, operand2 = self.eval_operands(statement, level)
        return int(operand1) + int(operand2)

    ##############################################
    
    def eval_SaturatedAddition(self, statement, level):
        
        operand1, operand2 = self.eval_operands(statement, level)
        return max(operand1 + operand2, statement.operand_sup)
    
    ##############################################

    def eval_Subtraction(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 - operand2

    ##############################################
    
    def eval_SaturatedSubtraction(self, statement, level):
        
        operand1, operand2 = self.eval_operands(statement, level)
        return min(operand1 - operand2, 0)
    
    ##############################################

    def eval_Multiplication(self, statement, level):
        
        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 * operand2

    ##############################################

    def eval(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 // operand2

    ##############################################

    def eval_And(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 & operand2

    ##############################################

    def eval_Or(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 | operand2

    ##############################################

    def eval_Xor(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return xor(int(operand1), int(operand2), operand1.cell_size)

    ##############################################

    def eval_LeftShift(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 << operand2

    ##############################################

    def eval_RightShift(self, statement, level):

        operand1, operand2 = self.eval_operands(statement, level)
        return operand1 >> operand2

####################################################################################################
# 
# End
# 
####################################################################################################
