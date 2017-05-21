================
Code Refactoring
================

C Language
==========

Standards:

* ANSI C
* `N1256: Final draft of the C99 standard
  <http://www.open-std.org/jtc1/sc22/WG14/www/docs/n1256.pdf>`_
* `ISO/IEC 9899 documents <http://www.open-std.org/JTC1/SC22/WG14/www/standards>`_
* `N1570: Final draft of the C1X standard
  <http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf>`_

ANSI C (C88) Features:

* const

C99 Features:

* inline
* long long int
* support for one-line comments //

Implementations:

* `Visual Studio C Language Reference <https://msdn.microsoft.com/en-us/library/fw5abdx6.aspx>`_

Intermediate Variable for Structure Access
==========================================

Write intermediate variable for structure access like::

  a[b].c->b

It makes the code more readble and help the compilator, but it has drawbacks:

* add lines for the intermediate variables
* require ``&(...)`` to get struct pointer

Macros
======

Test a bit::

  #define TestBit(value, i) value & (1 << i)

Value of a bit::

  #define BitValue(value, i) (value >> i) & 1

Value against a mask (masked value ...)::

  (A & ~mask) | (B & mask)

addr > 31 && addr < 31 + MAX_IOs

(avr->flash[pc + 1] << 8) | avr->flash[pc]

.. End
