===========================
Instruction Set YAML Format
===========================

Example::

     ADC:
       description: Add with Carry
       alternate: Add with Carry two Registers
       operations:
         -
           opcode: 0001 11rd dddd rrrr
           operands: [Rd, Rr]
           operation:
             R = Rd + Rr + C
             H = Rd3•Rr3 + (Rd3 + Rr3)•¬R3
             C = Rd7•Rr7 + (Rd7 + Rr7)•¬R7
             V = Rd7•Rr7•¬R7 + ¬Rd7•¬Rr7•R7
             N = R7
             Z = R == 0
             S = N ⊗ V
             Rd = R
           flags: [Z, C, N, V, H]
           cycles: 1

    AND:
      description: Logical AND
      alternate: Logical AND Registers
      operations:
        -
          opcode: 0010 00rd dddd rrrr
          operands: [Rd, Rr]
          operation: Rd = Rd & Rr
          flags: [Z, N, V]
          cycles: 1

    TST:
      description: Test for Zero or Minus
      alias_of: AND
      alias_substitution: Rr = Rd

Format::

    INSTRUCTION:
      description: description text
      alternate: optional alternate description
      alias_of: only for instruction which are an alias of an instruction
      alias_substitution: operand substitution
      operations:
        -
          opcode: opcode encoding
          operands: list of operands
          operation: operations in HDL
          flags: list of flags that could be modified by the instruction
          cycles: number of cycles
