=============
AVR Datasheet
=============

.. toctree::
  :hidden:

  atmega-640-1280-2560.register-summary

This part contains a subtract of Atmel datasheets on AVR.

How to Extract Data from Atmel Datasheets
=========================================

There is two possibilities to extract data from datasheet, the first one is to copy text using a PDF
viewer, and the second one is to dump the PDF text content using a tool like *pdftotext*.  Then use
a mixture of scripts and a powerful editor to cleanup and reformat the text, a spreadsheet like
Libre Office can help to deal with tables through a CSV file.

AVR Registers
=============

SREG – AVR Status Register
--------------------------

The AVR Status Register – SREG – is defined as:

============= === === === === === === === === ====
Bit           7   6   5   4   3   2   1   0
0x3F (0x5F)   I   T   H   S   V   N   Z   C   SREG
Read/Write    R/W R/W R/W R/W R/W R/W R/W R/W
Initial Value 0   0   0   0   0   0   0   0
============= === === === === === === === === ====

Bit 7 – I: Global Interrupt Enable
  The Global Interrupt Enable bit must be set for the interrupts to be enabled. The individual
  interrupt enable control is then performed in separate control registers. If the Global Interrupt
  Enable Register is cleared, none of the inter- rupts are enabled independent of the individual
  interrupt enable settings. The I-bit is cleared by hardware after an interrupt has occurred, and
  is set by the RETI instruction to enable subsequent interrupts. The I-bit can also be set and
  cleared by the application with the SEI and CLI instructions.

Bit 6 – T: Bit Copy Storage
  The Bit Copy instructions BLD (Bit LoaD) and BST (Bit STore) use the T-bit as source or
  destination for the oper- ated bit. A bit from a register in the Register File can be copied into
  T by the BST instruction, and a bit in T can be copied into a bit in a register in the Register
  File by the BLD instruction.

Bit 5 – H: Half Carry Flag
  The Half Carry Flag H indicates a Half Carry in some arithmetic operations. Half Carry Is useful
  in BCD arithmetic.

Bit 4 – S: Sign Bit, S = N ⊕ V
  The S-bit is always an exclusive or between the Negative Flag N and the Two’s Complement Overflow
  Flag V.

Bit 3 – V: Two’s Complement Overflow Flag
  The Two’s Complement Overflow Flag V supports two’s complement arithmetics.

Bit 2 – N: Negative Flag
  The Negative Flag N indicates a negative result in an arithmetic or logic operation.

Bit 1 – Z: Zero Flag
  The Zero Flag Z indicates a zero result in an arithmetic or logic operation.

Bit 0 – C: Carry Flag
  The Carry Flag C indicates a carry in an arithmetic or logic operation.

General Purpose Register File
-----------------------------

The AVR has 32 8-bit general purpose registers which are mapped at the beginning of the SRAM memory
space. The last registers (R26-R31) can be grouped by two to form three 16-bit registers called X, Y
and Z.

==== ===== ====================
Name Addr.
R0   0x00
R1   0x01
R2   0x02
...
R13  0x0D
R14  0x0E
R15  0x0F
R16  0x10
R17  0x11
...
R26  0x1A  X-register Low Byte 
R27  0x1B  X-register High Byte
R28  0x1C  Y-register Low Byte 
R29  0x1D  Y-register High Byte
R30  0x1E  Z-register Low Byte 
R31  0x1F  Z-register High Byte
==== ===== ====================

Stack Pointer
-------------

The AVR Stack Pointer is implemented as two 8-bit registers in the I/O space. The number of bits actually used is
implementation dependent. Note that the data space in some implementations of the AVR architecture is so small
that only SPL is needed. In this case, the SPH Register will not be present.

============= ==== ==== ==== ==== ==== ==== === ==== ===
Bit           15   14   13   12   11   10   9   8
0x3E (0x5E)   SP15 SP14 SP13 SP12 SP11 SP10 SP9 SP8  SPH
0x3D (0x5D)   SP7  SP6  SP5  SP4  SP3  SP2  SP1 SP0  SPL
Bit           7    6    5    4    3    2    1    0
Read/Write    R/W  R/W  R/W  R/W  R/W  R/W  R/W  R/W
...           R/W  R/W  R/W  R/W  R/W  R/W  R/W  R/W
Initial Value 0    0    1    0    0    0    0    1
...           1    1    1    1    1    1    1    1
============= ==== ==== ==== ==== ==== ==== === ==== ===

RAMPZ – Extended Z-pointer Register for ELPM/SPM
------------------------------------------------

============= ====== ====== ====== ====== ====== ====== ====== ====== =====
Bit           7      6      5      4      3      2      1      0
0x3B (0x5B)   RAMPZ7 RAMPZ6 RAMPZ5 RAMPZ4 RAMPZ3 RAMPZ2 RAMPZ1 RAMPZ0 RAMPZ
Read/Write    R/W    R/W    R/W    R/W    R/W    R/W    R/W    R/W
Initial Value 0      0      0      0      0      0      0      0
============= ====== ====== ====== ====== ====== ====== ====== ====== =====

For ELPM/SPM instructions, the Z-pointer is a concatenation of RAMPZ, ZH, and ZL. Note that LPM is
not affected by the RAMPZ setting.

The Z-pointer used by ELPM and SPM:

=============== ===== ==== ====
Bit             7-0   7-0  7-0
(Individually)  RAMPZ ZH   ZL
Bit (Z-pointer) 23-16 15-8 7-0
=============== ===== ==== ====

The actual number of bits is implementation dependent. Unused bits in an implementation will always
read as zero.  For compatibility with future devices, be sure to write these bits to zero.

EIND – Extended Indirect Register
---------------------------------

============= ===== ===== ===== ===== ===== ===== ===== ===== ====
Bit           7     6     5     4     3     2     1     0
0x3C (0x5C)   EIND7 EIND6 EIND5 EIND4 EIND3 EIND2 EIND1 EIND0 EIND
Read/Write    R/W   R/W   R/W   R/W   R/W   R/W   R/W   R/W
Initial Value 0     0     0     0     0     0     0     0
============= ===== ===== ===== ===== ===== ===== ===== ===== ====

For EICALL/EIJMP instructions, the Indirect-pointer to the subroutine/routine is a concatenation of
EIND, ZH, and ZL. Note that ICALL and IJMP are not affected by the EIND setting.

The Indirect-pointer used by EICALL and EIJMP:

====================== ===== ==== ===
Bit                    7-0   7-0  7-0
(Individually)         EIND  ZH   ZL
Bit (Indirect-pointer) 23-16 15-8 7-0
====================== ===== ==== ===

The actual number of bits is implementation dependent. Unused bits in an implementation will always
read as zero.  For compatibility with future devices, be sure to write these bits to zero.

AVR Memories
============

The program is stored in the Flash memory and the volatile data in the SRAM.

The structure of the SRAM memory space for devices having a large numbers of peripheral units like
the ATmega640/1280/1281/2560/2561 is the following:

====== ====== =================== ===================================================================
Addr.         Name
0x00   0x1F   Register File       32 General Purpose Registers
0x20   0x5F   I/O Memory          64 I/O accessible the using IN and OUT instructions
0x60   0x1FF  Extended I/O Memory 416 I/O accessible using the ST/STS/STD and LD/LDS/LDD instructions
0x200  0x21FF Internal SRAM       8192 x 8-bit located after the 512 reserved bytes
0x2200 0xFFFF External SRAM
====== ====== =================== ===================================================================

Register Summary
================

* :ref:`atmega-640-1280-2560-register-summary`

Instructions
============

.. toctree::

  instructions
  instruction-decision-tree

32-bit Instructions:

==== ====== ======
Name Opcode Mask
CALL 0x940e 0xfe0e
JMP  0x940c 0xfe0e
LDS  0x9000 0xfe0f
STS  0x9200 0xfe0f
==== ====== ======

Instructions without operand:

====== ======
BREAK  0x9598
CLC    0x9488
CLH    0x94d8
CLI    0x94f8
CLN    0x94a8
CLS    0x94c8
CLT    0x94e8
CLV    0x94b8
CLZ    0x9498
EICALL 0x9519
EIJMP  0x9419
ELPM   0x95d8
ICALL  0x9509
IJMP   0x9409
LPM    0x95c8
NOP    0x0000
RET    0x9508
RETI   0x9518
SEC    0x9408
SEH    0x9458
SEI    0x9478
SEN    0x9428
SES    0x9448
SET    0x9468
SEV    0x9438
SEZ    0x9418
SEZ    0x9588
SLEEP  0x9588
SPM    0x95e8
SPM    0x95f8
WDR    0x95a8
====== ======

Operand patterns:

================  =====
Pattern           Count
_2q1_1q2_1d5_1q3   2
_2q1_1q2_1r5_1q3   2
_4K4d4K4           7
_4k12              2
_5A2d5A4           1
_5A2r5A4           1
_5k3d4k4           2
_6d10              4
_6k7_3            18
_6k7s3             2
_6r1d5r4          12
_7d5_1b3           2
_7d5_4            25
_7k5_3k1           2
_7r5_1b3           2
_7r5_4            13
_8A5b3             4
_8K2d2K4           2
_8K4_4             1
_8d4_4             1
_8d4r4             2
_9d3_1r3           4
_9s3_4             2
================  =====

.. End
