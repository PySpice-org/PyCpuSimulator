====
Todo
====


Missing HEX Features
--------------------

* Automatic check against binutils disassembled hex [partially done: check mnemonic but not operands]
* Set a ROM and an instruction's map <P1>
* Handle data section (.word ???)

Missing Core Features
---------------------

* Implement bit mapped registers (cf. SREG) <P1>
  Attention to register name's clash: Z versus SREG[Z] versus Sz, HDL as register[bit]
* Implement concatenated 16-bit registers (cf. SPH/SPL, X/Y/Z etc.) ??? <P2>

Implement a basic CPU
---------------------

* Design an basic instruction set to test each feature
* Could use an AVR subset

How to implement the simulator
------------------------------

* Initialise an AST program (routine) for each opcodes (opcode indexed)
* Read an HEX to set the ROM: data and instructions
* ROM is indexed by PC
* for each opcode : execute the corresponding AST program, we need a mechanism to substitute the operands
  An AST program is thus a routine with arguments [partially done]

How to complete the AVR support
-------------------------------

* Check the AVR instruction set YAML files and translate operations in valid HDL (micro-code)
* MULS 16 <= d : do it in HDL ?
* IO registers (see extractor code)
* Much more challenging : simulate peripherals

----

* Implement PC
  PC corresponds to instruction index, not to micro-code
* plug instruction operation in core
* Run an hex
