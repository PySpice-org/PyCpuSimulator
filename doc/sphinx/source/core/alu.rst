
x xor y = (x + y) mod 2

==============
Floating Point
==============

* IEEE 754 double    64-bit: 1 sign | 11 exponent | fraction 52 (53)
* extended precision 80-bit: 1 sign | 15 exponent | 1 integer | fraction 63

===============
Binary Addition
===============

Half Adder
----------

A half adder adds two bits and generates the sum and an eventual carry.

Truth table:

=== === === ====
 a   b   C   S 
 0   0   0   0   
 0   1   0   1   
 1   0   0   1   
 1   1   1   0   
=== === === ====

::
    C = a ∧ b
    S = (¬a ∧ b) ∨ (a ∧ ¬b)
      = a ⊻ b

Full Adder
----------

A full adder uses a second stage to add the carry from the previous bit.

We substitute ``a → a ⊻ b, b → c`` in the second half adder and we add (or) the carries from the two
half adders::

    C = (a ∧ b) ∨ ((a ⊻ b) ∧ c)
    S = (a ⊻ b) ⊻ c

Truth table:

=== === === === ====
 a   b   c   C   S 
 0   0   0   0   0   
 0   1   0   0   1   
 1   0   0   0   1   
 1   1   0   1   0   
 0   0   1   0   1   
 0   1   1   1   0   
 1   0   1   1   0   
 1   1   1   1   1   
=== === === === ====

==================
Binary Subtraction
==================

::
   A - B = A - ¬B + 1

=====================
Binary Multiplication
=====================

     1011
   × 1110
   ──────
     0000
    1011 
   1011  
+ 1011   
─────────
 10011010

Réferences:

* Baugh–Wooley algorithm
* Wallace tree
* Booth encoding
* Dadda multiplier
