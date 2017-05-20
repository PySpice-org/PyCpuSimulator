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

import ply.lex as lex
import ply.yacc as yacc

####################################################################################################

from .CoreAst import *

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def ensure_statement_list(x):
    if isinstance(x, StatementList):
        return x
    else:
        return StatementList(x)

####################################################################################################

class Parser(object):

    _logger = _module_logger.getChild('Parser')

    ##############################################

    _operator_to_class = {operator_class.__operator__:operator_class
                          for operator_class in (
                                  Addition,
                                  And,
                                  Division,
                                  Equal,
                                  Greater,
                                  GreaterEqual,
                                  LeftShift,
                                  Less,
                                  LessEqual,
                                  Multiplication,
                                  NotEqual,
                                  Or,
                                  RightShift,
                                  Subtraction,
                                  Xor,
                          )
    }
    
    ##############################################

    reserved = {
        'if' : 'IF',
        'else' : 'ELSE',
    }
    
    tokens = [
        'SEMICOLON',
        'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS',
        'LEFT_BRACE', 'RIGHT_BRACE',
        'SET',         
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'AND', 'OR', 'XOR', 'LEFT_SHIFT', 'RIGHT_SHIFT',
        'EQUAL', 'NOT_EQUAL', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL',
        'LEFT_BRACKET', 'RIGHT_BRACKET', 'COMMA', 'COLON', 'BIT_RANGE', 
        'BINARY_NUMBER', 'OCTAL_NUMBER', 'HEX_NUMBER', 'DECIMAL_NUMBER',
        'AT', 'DOLLAR',
        'NAME',
    ] + list(reserved.values())

    ##############################################

    def t_error(self, token):
        self._logger.error("Illegal character '%s' at line %u and position %u" %
                           (token.value[0],
                            token.lexer.lineno,
                            token.lexer.lexpos - self._previous_newline_position))
        # token.lexer.skip(1)
        raise NameError('Lexer error')

    ##############################################

    t_ignore  = ' \t'

    def t_newline(self, t):
        r'\n+'
        # Track newline
        t.lexer.lineno += len(t.value)
        self._previous_newline_position = t.lexer.lexpos
        # t.type = 'SEMICOLON'
        # return t
        
    t_ignore_COMMENT = r'\#[^\n]*'
    
    ##############################################

    t_SEMICOLON = r';'

    t_LEFT_PARENTHESIS = r'\('
    t_RIGHT_PARENTHESIS = r'\)'

    t_LEFT_BRACE = r'\{'
    t_RIGHT_BRACE = r'\}'
    
    t_SET = r'='
    
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'

    t_AND = r'&' # was .
    t_OR = r'\|'
    t_XOR = r'\^'
    t_LEFT_SHIFT = r'<<'
    t_RIGHT_SHIFT = r'>>'

    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_LESS = r'<'
    t_GREATER = r'>'
    t_LESS_EQUAL = r'<='
    t_GREATER_EQUAL = r'>='
                
    t_LEFT_BRACKET = r'\['
    t_RIGHT_BRACKET = r'\]'
    t_COMMA = r','
    t_COLON = r':'
    t_BIT_RANGE = r'\.\.'

    t_AT = r'@'
    t_DOLLAR = r'\$'
    
    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check for reserved words
        t.type = self.reserved.get(t.value, 'NAME')
        return t

    def t_BINARY_NUMBER(self, t):
        r'0b(0|1)+'
        t.value = int(t.value, 2)
        return t

    def t_OCTAL_NUMBER(self, t):
        r'0o[0-7]+'
        t.value = int(t.value, 8)
        return t

    def t_HEX_NUMBER(self, t):
        r'0x[0-9a-fA-F]+'
        t.value = int(t.value, 16)
        return t

    def t_DECIMAL_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    ##############################################
    #
    # Grammar
    #

    # from lowest
    precedence = (
        ('left', 'COMMA'),
        ('left', 'EQUAL'),
        ('left', 'OR'),
        ('left', 'XOR'),
        ('left', 'AND'),
        ('left', 'EQUAL', 'NOT_EQUAL'),
        ('left', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL'),
        ('left', 'LEFT_SHIFT', 'RIGHT_SHIFT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'LEFT_BRACKET', 'RIGHT_BRACKET'),
        # ('left', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS'),
    )

    def p_error(self, p):
        self._logger.error("Syntax error at '%s'", p.value)
        raise NameError('Parser error')
    
    start = 'program'

    def p_empty(self, p):
        'empty :'
        pass
    
    def p_program(self, p):
        '''program : statement
                   | program statement
                   | empty
        '''
        if len(p) == 3:
            statement = p[2]
        else:
            statement = p[1]
        if statement is not None:
            self._program.add(statement)

    def p_statement(self, p):
        '''statement : expression_statement
                     | compound_statement
                     | if_statement
        '''
        p[0] = p[1]
            
    def p_expression_statement(self, p):
        '''expression_statement : assignation SEMICOLON
                                | function SEMICOLON
                                | SEMICOLON
        '''
        if len(p) == 3:
            p[0] = p[1]

    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement
        '''
        if len(p) == 3:
            p[1].add(p[2])
            p[0] = p[1]
        else:
            p[0] = StatementList(p[1])
            
    def p_compound_statement(self, p):
        '''compound_statement : LEFT_BRACE statement_list RIGHT_BRACE
                              | LEFT_BRACE RIGHT_BRACE
        '''
        if len(p) == 4:
            p[0] = p[2]

    def p_if_statement(self, p):
        '''if_statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement
        | IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement ELSE statement
        '''
        condition = p[3]
        then_expression = ensure_statement_list(p[5])
        if len(p) == 8:
            else_expression = ensure_statement_list(p[7])
            p[0] = If(condition, then_expression, else_expression)
        else:
            p[0] = If(condition, then_expression)

    def p_expression_list(self, p):
        '''expression_list : expression
                           | expression_list COMMA expression
        '''
        if len(p) == 3:
            p[1].add(p[2])
            p[0] = p[1]
        else:
            p[0] = StatementList(p[1])
            
    def p_function(self, p):
        '''function : NAME LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                    | NAME LEFT_PARENTHESIS RIGHT_PARENTHESIS
        '''
        if len(p) == 5:
            p[0] = Function(p[1], p[3])
        else:
            p[0] = Function(p[1])
            
    def p_assignation(self, p):
        'assignation : destination SET expression'
        p[0] = Assignation(p[3], p[1]) # eval value first

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
        # | NAME LEFT_BRACKET NAME COMMA NAME RIGHT_BRACKET
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
                      | expression EQUAL expression
                      | expression NOT_EQUAL expression
                      | expression LESS expression
                      | expression GREATER expression
                      | expression LESS_EQUAL expression
                      | expression GREATER_EQUAL expression
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
