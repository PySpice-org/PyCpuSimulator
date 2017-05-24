===================
Micro Code Language
===================

Name: [a-zA-Z_][a-zA-Z_0-9]*

Number:

* binary:     0b(0|1)+
* decimal:    0o[0-7]+
* hexdecimal: 0x[0-9a-fA-F]+
* decimal:    \d+

BNF Grammar::

    empty :

    program : statement
            | program statement
            | empty

    statement : expression_statement
              | compound_statement
              | if_statement

    expression_statement : assignation ;
                         | function ;
                         | ;

    statement_list : statement
                   | statement_list statement

    compound_statement : { statement_list }
                       | { }

    if_statement : IF ( expression ) statement
                 | IF ( expression ) statement ELSE statement

    expression_list : expression
                    | expression_list , expression

    function : NAME ( expression_list )
             | NAME ( )

    assignation : destination = expression

    destination : register
                | register_concatenation
                | register_bit
                | register_bit_range
                | addressing

    constant : DECIMAL_NUMBER
             | BINARY_NUMBER
             | OCTAL_NUMBER
             | HEX_NUMBER

    register : NAME

    register(_operand) : @ NAME

    constant(_operand) : $ NAME

    register_concatenation : register : register

    register_bit : register [ expression ]

    register_bit_range : register [ constant .. constant ]

    addressing : [ expression ]

    expression : register
               | register_concatenation
               | register_bit
               | register_bit_range
               | addressing
               | constant

    expression : expression + expression
               | expression - expression
               | expression * expression
               | expression / expression
               | expression & expression
               | expression | expression
               | expression > expression
               | expression << expression
               | expression >> expression
               | expression == expression
               | expression != expression
               | expression < expression
               | expression > expression
               | expression <= expression
               | expression >= expression

Examples::

  # increment register Y
  Y = Y + 1

  # add register operand d with constant operand k (d and k are relative to the instruction)
  @d = @d + $k
