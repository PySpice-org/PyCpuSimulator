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

"""

Micro Code Language
-------------------

ASCII symbols are:

* `` ` ``
* ``!``
* ``"``
* ``#`` comment
* ``$``
* ``%``
* ``&`` and
* ``'``
* ``()``
* ``*`` multiplication
* ``+`` addition
* ``,``
* ``-`` subtraction
* ``.`` floating point
* ``/`` division
* ``:``
* ``;`` statement separator
* ``< >``
* ``=``
* ``?``
* ``@``
* ``[]`` addressing
* ``\``
* ``^``
* ``_`` allowed in name
* ``{}``
* ``|`` or
* ``~`` not

Compounds:

* ``++`` increment
* ``--`` decrement
* ``//``
* ``<=`` inferior equal 
* ``==`` equal
* ``>=`` superior equal
* ``->`

Ambiguous:

* ``<-``

"""

####################################################################################################

import logging

####################################################################################################

import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN

####################################################################################################

from .CoreAst import *

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Parser(object):

    _logger = _module_logger.getChild('Parser')

    ##############################################

    _operator_to_class = {operator_class.__operator__:operator_class
                          for operator_class in (
                                  Addition,
                                  Subtraction,
                                  Multiplication,
                                  Division,
                                  And,
                                  Or,
                                  Xor,
                                  LeftShift,
                                  RightShift,
                          )
    }
    
    ##############################################

    reserved = {
        'if' : 'IF',
        'then' : 'THEN',
        'else' : 'ELSE',
    }
    
    tokens = [
        'SEMICOLON',
        'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS',
        'SET',         
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'AND', 'OR', 'XOR', 'LEFT_SHIFT', 'RIGHT_SHIFT', 'EQUALS',
        'LEFT_BRACKET', 'RIGHT_BRACKET', 'COLUMN', 'COLON', 'BIT_RANGE', 
        'BINARY_NUMBER', 'OCTAL_NUMBER', 'HEX_NUMBER', 'DECIMAL_NUMBER',
        'AT', 'DOLLAR',
        'NAME',
    ] + list(reserved.values())

    # Declare the lexer states
    # states = (
    #     )

    ##############################################

    def t_ANY_error(self, token):
        self._logger.error("Illegal character '%s' at line %u and position %u" %
                           (token.value[0],
                            token.lexer.lineno,
                            token.lexer.lexpos - self._previous_newline_position))
        # token.lexer.skip(1)
        raise NameError('Lexer error')

    ##############################################

    t_ignore  = ' \t'

    def t_ANY_newline(self, token):
        r'\n+'
        # Track newline
        token.lexer.lineno += len(token.value)
        self._previous_newline_position = token.lexer.lexpos

    t_ignore_COMMENT = r'\#.*' # Fixme: newline ?
    
    ##############################################

    t_SEMICOLON = r';'

    t_LEFT_PARENTHESIS = r'\('
    t_RIGHT_PARENTHESIS = r'\)'

    t_SET = r'<-'
    
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'

    t_AND = r'&' # was .
    t_OR = r'\|'
    t_XOR = r'\|!'
    t_LEFT_SHIFT = r'<<'
    t_RIGHT_SHIFT = r'>>'
    t_EQUALS = r'=='

    t_LEFT_BRACKET = r'\['
    t_RIGHT_BRACKET = r'\]'
    t_COLUMN = r','
    t_COLON = r':'
    t_BIT_RANGE = r'\.\.'

    t_AT = r'@'
    t_DOLLAR = r'\$'
    
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    def t_BINARY_NUMBER(self, t):
        r'0b(0|1)+'
        # try:
        t.value = int(t.value, 2)
        # except ValueError:
        return t

    def t_OCTAL_NUMBER(self, t):
        r'0o[0..7]+'
        # try:
        t.value = int(t.value, 8)
        # except ValueError:
        return t

    def t_HEX_NUMBER(self, t):
        r'0x[0..9a..fA..F]+'
        # try:
        t.value = int(t.value, 16)
        # except ValueError:
        return t

    def t_DECIMAL_NUMBER(self, t):
        r'\d+'
        # try:
        t.value = int(t.value)
        # except ValueError:
        return t
    
    ##############################################
    #
    # Grammar
    #

    # precedence = (
    #     ('left','PLUS','MINUS'),
    #     ('left','TIMES','DIVIDE'),
    #     ('right','UMINUS'),
    # )

    def p_error(self, p):
        self._logger.error("Syntax error at '%s'", p.value)
        raise NameError('Parser error')
    
    start = 'program'

    def p_empty(self, p):
        'empty :'
        pass
    
    def p_program(self, p):
        '''program : assignation
                   | assignation SEMICOLON program
                   | empty
        '''
        statement = p[1]
        if statement is not None:
            self._program.add(statement) # Fixme: reversed for ... ; ...
    
    def p_assignation(self, p):
        'assignation : destination SET expression'
        p[0] = Assignation(p[1], p[3])

    def p_destination(self, p):
        # R
        # Xh:Xl
        # R[b]
        # R[b..b]
        # [...]
        # IO[P, b]
        '''destination : register
                       | register_concatenation
                       | register_bit
                       | register_bit_range
                       | addressing
        '''
        # | NAME LEFT_BRACKET NAME COLUMN NAME RIGHT_BRACKET
        p[0] = p[1]
    
    def p_number(self, p):
        # constant
        '''constant : DECIMAL_NUMBER
                    | BINARY_NUMBER
                    | OCTAL_NUMBER
                    | HEX_NUMBER
        '''
        p[0] = Constant(p[1])
    
    def p_register(self, p):
        # R
        '''register : NAME
        '''
        p[0] = Addressing('REGISTER', Register(p[1]))

    def p_register_operand(self, p):
        # R
        '''register : AT NAME
        '''
        p[0] = RegisterOperand(p[2])

    def p_constant_operand(self, p):
        # R
        '''constant : DOLLAR NAME
        '''
        p[0] = ConstantOperand(p[2])
        
    def p_register_concatenation(self, p):
        # Xh:Xl
        '''register_concatenation : register COLON register
        '''
        p[0] = Concatenation(p[1], p[3])
   
    def p_register_bit(self, p):
        # R[b]
        '''register_bit : register LEFT_BRACKET expression RIGHT_BRACKET
        '''
        p[0] = Bit(p[1], p[3])

    def p_register_bit_range(self, p):
        # R[b..b]
        '''register_bit_range : register LEFT_BRACKET constant BIT_RANGE constant RIGHT_BRACKET
        '''
        p[0] = BitRange(p[1], p[3], p[5])

    def p_addressing(self, p):
        # [ ... ]
        '''addressing : LEFT_BRACKET expression RIGHT_BRACKET
        '''
        p[0] = Addressing('RAM', p[2])

    def p_source(self, p):
        '''expression : register
                      | register_concatenation
                      | register_bit
                      | register_bit_range
                      | addressing
                      | constant
        '''
        p[0] = p[1]
    
    def p_binary_operation(self, p):
        # ... OP ...
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression AND expression
                      | expression OR expression
                      | expression XOR expression
                      | expression LEFT_SHIFT expression
                      | expression RIGHT_SHIFT expression
        '''
        p[0] = self._operator_to_class[p[2]](p[1], p[3])    
    
    ##############################################

    def __init__(self):

        self._build()

    ##############################################

    def _build(self, **kwargs):

        self._lexer = lex.lex(module=self, **kwargs)
        self._parser = yacc.yacc(module=self, **kwargs)

    ##############################################

    def _reset(self):

        self._previous_newline_position = 0
        self._program = Program()
        
    ##############################################

    def parse(self, text):

        self._reset() # Fixme: after ?
        self._parser.parse(text, lexer=self._lexer)
        return self._program
        
    ##############################################

    def test_lexer(self, text):

        self._reset()
        self._lexer.input(text)
        while True:
            token = self._lexer.token()
            if not token:
                break
            print(token)

####################################################################################################
# 
# End
# 
####################################################################################################
