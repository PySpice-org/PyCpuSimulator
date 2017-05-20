simavr - 8 Bit AVR simulator
============================

Supported Cores
---------------

* ATMega 48/88/168/328
* ATMega 164/324/644
* ATMega128
* ATTiny 25/45/85
* ATTiny2313
* ATTiny13

Supported Peripherals
---------------------

* EEProm

  * Load from ELF file, and allow re-programming from the firmware

* Watchdog Timer

  * With WDT instruction support

* Flash Self Programming

  * Support for the Arduino bootloader

* 8 and 16 Bits Timers

  * Normal Mode (mode zero)
  * CDC Mode (with interupts)
  * Fast PWM Mode
  * TCNT reading/writing
  * Some mode using the ICR
  * Input Capture, proper
  * TODO Phase Correct PWM Mode
    
* UART

  * RX/TX Interrupts
  * External FIFO
  * Baud calculation
  * Flow Control for external code
  * TODO UART in SPI mode.

* SPI

  * Master with interrupt
  * Slave
* IO Ports

  * PCINT all working

* External Interrupts
  
  * All hooked up to proper IO Port pins

* ADC

  * Core Voltages can be set in the ELF file
  * ADC simavr module handles conversion to millivolts

Unsupported Peripherals
-----------------------

* TODO Analog Comparator
* TODO Main Clock divider calculation
* TODO TWI/i2c - In progress

Extras
------

* GDB support

  * Can run in "active mode" (CPU stopped until connection)
  * Can run in "passive mode" (gdb is not activated until a crash)
  * Can run in "AVR" mode (gdb server is launched if AVR used "BREAK" instruction)
  * Can be totaly disabled too, but given the useful passive mode, theres no real need.

* VCD Waveform File Creator

  * Up to 32 traces per files
  * No practical limits how many files are open (20+)
  * Used Internal IRQs so is non-intrusive

* ELF file loader

  * Load the .eeprom section
  * Special ELF section contains TAGS that can pass parameters to the emulator, without changing the
    compilation options for the firmware.
  * CPU Name Tag
  * CPU Base Frequency Tag
  * CPU Voltages for VCC/AVCC/AREF (For the ADC source voltage)
  * VCD File Name Tag
  * ADD a VCD trace (IO Register only!) Tag
  * Specify a "command path" to send commands to simavr from the firmware (!)

* IHEX file loader

  * Supports multiple section in HEX (flash, eeprom & fuses)

