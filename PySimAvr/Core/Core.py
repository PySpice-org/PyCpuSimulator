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

class NamedObject(object):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name
    
####################################################################################################
        
class Memory(NamedObject):

    ##############################################    

    def __init__(self, name, cell_size):

        super(Memory, self).__init__(name)
        self._cell_size = cell_size

    ##############################################

    @property
    def cell_size(self):
        return self._cell_size

    ##############################################

    @property
    def inf(self):
        return 0
    
    ##############################################

    @property
    def sup(self):
        return 2**self._cell_size -1

    ##############################################

    def check_value(self, value):
        if value < self.inf or value > self.sup:
            raise ValueError("Value is out of range")
    
    ##############################################

    def truncate(self, value):
        # Numpy array performs this action natively
        # return value &_self.sup
        return value % 2**self._cell_size

    ##############################################

    def two_complement(self, value):
        self.check_value(value)
        return self.sup - value # +1 ?
    
    ##############################################

    @property
    def np_dtype(self):
        
        if self._cell_size == 8:
            return np.uint8
        elif self._cell_size == 16:
            return np.uint16
        elif self._cell_size == 32:
            return np.uint32
        elif self._cell_size == 64:
            return np.uint64
        else:
            raise ValueError("Wrong data size")

####################################################################################################

class MemoryValueMixin(object):

    ##############################################

    def two_complement(self):
        return self.sup - int(self) # +1?

####################################################################################################

class Register(MemoryValueMixin, Memory):

    __cell_size__ = None
    
    ##############################################    

    def __init__(self, name, cell_size=None):

        if cell_size is None:
            cell_size = self.__cell_size__
        
        Memory.__init__(self, name, cell_size)
        
        self._dtype = self.np_dtype
        self._value = self._dtype(0)
        
    ##############################################

    def reset(self):
        self._value = self._dtype(0)

    ##############################################

    def __int__(self):
        # make a copy
        # TypeError: __int__ returned non-int (type numpy.uint8)
        # return self._dtype(self._value) 
        return int(self._value)

    ##############################################

    def set(self, value):
        self._value = self._dtype(value)

    ##############################################

    def str_value(self):
        return "{} = 0x{:X}".format(self._name, self._value)
    
####################################################################################################
    
class Register8(Register):
  __cell_size__ = 8

class Register16(Register):
  __cell_size__ = 16
  
class Register32(Register):
  __cell_size__ = 32

class Register64(Register):
  __cell_size__ = 64


####################################################################################################

class MappedRegister(MemoryValueMixin, Memory):

    ##############################################    

    def __init__(self, name, memory_cell):

        Memory.__init__(self, name, memory_cell.cell_size)
        self._memory_cell = memory_cell

    ##############################################

    def reset(self):
        self._memory_cell.set(0)

    ##############################################

    def __int__(self):
        return int(self._memory_cell)

    ##############################################

    def set(self, value):
        self._memory_cell.set(value)

    ##############################################

    def __str__(self):
        return self._name + ' / ' + str(self._memory_cell)
        
    ##############################################

    def str_value(self):
        return self._name + ' / ' + self._memory_cell.str_value()

####################################################################################################

class RegisterFile(NamedObject):

    ##############################################    

    def __init__(self, name, registers):

        super(RegisterFile, self).__init__(name)

        self._registers = OrderedDict([(register.name, register)
                                       for register in registers])

    ##############################################

    def reset(self):

        for register in self._registers.values():
            register.reset()

    ##############################################

    def cell(self, register):
        return self._registers[register]

    ##############################################

    def __getitem__(self, register):
        return self._registers[register]

    ##############################################

    def __setitem__(self, register, value):
        self._registers[register].set(value)

    ##############################################

    def dump(self):

        # for register in self._registers.values():
        #     print(register)
        print(' | '.join([register.str_value() for register in self._registers.values()]))

####################################################################################################

class MemoryCell(MemoryValueMixin):

    ##############################################

    def __init__(self, memory, address):

        self._memory = memory
        self._address = address

    ##############################################

    @property
    def memory(self):
        return self._memory

    @property
    def address(self):
        return self._address

    @property
    def cell_size(self):
        return self._memory.cell_size
    
    ##############################################

    def __int__(self):
        return int(self._memory[self._address])

    ##############################################

    def set(self, value):
        self._memory[self._address] = value

    ##############################################

    def __str__(self):
        return "{}[0x{:x}]".format(self._memory.name, int(self._address))

    ##############################################

    def str_value(self):
        return str(self) + " = 0x{:X}".format(int(self))
    
####################################################################################################

class RomMemory(Memory):

    ##############################################    

    def __init__(self, name, cell_size, size, data=None):

        super(RomMemory, self).__init__(name, cell_size)

        self._memory = np.zeros(size, dtype=self.np_dtype)
        if data is not None:
            self._memory[...] = data
    
    ##############################################

    @property
    def size(self):
        return self._memory.shape[0]

    ##############################################

    def cell(self, address):
        return MemoryCell(self, address)
    
    ##############################################

    def __getitem__(self, address_slice):

        return self._memory[address_slice]
        
####################################################################################################

class RamMemory(RomMemory):

    ##############################################

    def reset(self):

        self._memory[...] = 0
    
    ##############################################

    def __setitem__(self, address_slice, value):

        self._memory[address_slice] = value

####################################################################################################

class Core(object):

    _logger = _module_logger.getChild('Core')
    
    ##############################################

    def __init__(self, memories):

        self._memories = {memory.name:memory for memory in memories}

        self._cycles = 0 # could be a register
        self._modified_registers = set()
        
    ##############################################

    @property
    def memory(self):
        return self._memories # Fixme:

    ##############################################

    @property
    def cycles(self):
        return self._cycles

    ##############################################

    def reset_trackers(self):

        self._modified_registers = set()
    
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

    def split_operand_by_type(self, operands):

        registers = []
        constants = []
        for operand in operands:
            if isinstance(operand, int):
                constants.append(operand)
            else: # Register or MemoryCell
                registers.append(operand)

        return registers, constants

    ##############################################

    def check_for_register_operand(self, *operands):

        registers, constants = self.split_operand_by_type(operands)
        if not registers:
            raise NameError("Forbidden operation, at least one register operand is required")
        else:
            return registers
        
    ##############################################

    def eval_statement(self, level, statement):

        self._logger.debug('')
        
        statement_class = statement.__class__.__name__
        print('  '*level + statement_class, statement)
        if statement_class == 'Function':
            statement_class = statement.name
        evaluator = getattr(self, 'eval_' + statement_class)
        if hasattr(statement, 'iter_on_operands'):
            # Compute the operand values: traverse recursively the AST
            args=  [self.eval_statement(level+1, operand)
                    for operand in statement.iter_on_operands()]
            value = evaluator(level, statement, *args)
        else:
            value = evaluator(level, statement)
            
        if value is not None:
            if isinstance(value, int):
                value_string = hex(value)
            else:
                value_string = str(value)
            print('  '*(level+1) + '=', str(value_string))

        return value
    
    ##############################################
    
    def run_ast_program(self, program):

        for statement in program:
            print()
            self.eval_statement(0, statement)
            print(' | '.join([register.str_value() for register in self._modified_registers]))
            # self.memory['REGISTER'].dump()
            self.reset_trackers()
            
    ##############################################

    def eval_If(self, level, statement):

        if self.eval_statement(level +1, statement.condition):
            branch = statement.then_expression
        else:
            branch = statement.else_expression
        if branch:
            for statement in branch:
                print()
                self.eval_statement(level +1, statement)

####################################################################################################

class StandardCore(Core):

    """This class implements a standard core with a very felxible ALU. For example we can add directly
    two constants.

    ALU operations are performed using Python integer. The value is truncated to the data type in
    the Numpy cell.

    """
    
    ##############################################
        
    def eval_Constant(self, level, statement):

        # Return the constant value
        # Fixme: wrap constant in a class ?
        return int(statement)

    ##############################################
        
    def eval_Register(self, level, statement):

        # Return the register name
        return str(statement)

    ##############################################
    
    def eval_Assignation(self, level, statement, value, cell):

        self._logger.debug('')

        int_value = int(value)
        # int_value = cell.truncate(int_value)
        cell.set(value)
        self._modified_registers.add(cell)
        print('  '*(level+1) + '{} <- 0x{:x}'.format(cell, int_value))
    
    ##############################################

    def eval_Addressing(self, level, statement, address):

        self._logger.debug('')

        # Return a register instance, use int(register) to retrieve the value
        memory = self.memory[statement.memory]
        # return memory[address]
        return memory.cell(address)
    
    ##############################################
        
    def eval_Concatenation(self, level, statement, operand1, operand2):

        # operand2 must be a register
        return int(operand1) << operand2.cell_size + int(operand2)

    ##############################################

    def eval_Bit(self, level, statement, operand1, operand2):

        return (int(operand1) >> int(operand2)) & 0x1

    ##############################################
    
    def eval_BitRange(self, level, statement, operand1, operand2, operand3):

        value2 = int(operand2)
        mask = 2**(int(operand3) - value2 +1) -1
        return (int(operand1) >> value2) & mask

    ##############################################    

    def eval_LowerNibble(self, level, statement, operand1):

        return int(operand1) & 0x0F

    ##############################################

    def eval_UpperNibble(self, level, statement, operand1):

        return (int(operand1) >> 4) & 0x0F

    ##############################################
    
    def eval_Addition(self, level, statement, operand1, operand2):
        
        return int(operand1) + int(operand2)

    ##############################################
    
    def eval_SaturatedAddition(self, level, statement, operand1, operand2):

        # operand1 must be a register
        return max(int(operand1) + int(operand2), operand1.sup)
    
    ##############################################

    def eval_Subtraction(self, level, statement, operand1, operand2):

        return int(operand1) - int(operand2)

    ##############################################
    
    def eval_SaturatedSubtraction(self, level, statement, operand1, operand2):
        
        return min(int(operand1) - int(operand2), 0)
    
    ##############################################

    def eval_Multiplication(self, level, statement, operand1, operand2):
        
        return int(operand1) * int(operand2)

    ##############################################

    def eval_Division(self, level, statement, operand1, operand2):

        return int(operand1) // int(operand2)

    ##############################################

    def eval_TwoComplement(self, level, statement, operand1):

        return operand1.two_complement()
    
    ##############################################

    def eval_And(self, level, statement, operand1, operand2):

        return int(operand1) & int(operand2)

    ##############################################

    def eval_Or(self, level, statement, operand1, operand2):

        return int(operand1) | int(operand2)

    ##############################################

    def eval_Xor(self, level, statement, operand1, operand2):

        return int(operand1) ^ int(operand2)
        
    ##############################################

    def eval_LeftShift(self, level, statement, operand1, operand2):

        # Fixme: -> ShiftLeft
        
        return int(operand1) << int(operand2)

    ##############################################

    def eval_RightShift(self, level, statement, operand1, operand2):

        return int(operand1) >> int(operand2)

    ##############################################

    def eval_RotateRight(self, level, statement, operand1, operand2):

        cell_size = operand1.cell_size
        rotation = int(operand2) % cell_size
        value = int(operand1)
        return value >> rotation | value << (cell_size - rotation)

    ##############################################

    def eval_Equal(self, level, statement, operand1, operand2):

        return int(operand1) == int(operand2)

    ##############################################

    def eval_NotEqual(self, level, statement, operand1, operand2):

        return int(operand1) != int(operand2)

    ##############################################

    def eval_Less(self, level, statement, operand1, operand2):

        return int(operand1) < int(operand2)

    ##############################################

    def eval_Greater(self, level, statement, operand1, operand2):

        return int(operand1) > int(operand2)

    ##############################################

    def eval_LessEqual(self, level, statement, operand1, operand2):

        return int(operand1) <= int(operand2)

    ##############################################

    def eval_GreaterEqual(self, level, statement, operand1, operand2):

        return int(operand1) >= int(operand2)

    ##############################################

    # Signed operations
    # Arithmetic Shift Instructions
    
####################################################################################################
# 
# End
# 
####################################################################################################
