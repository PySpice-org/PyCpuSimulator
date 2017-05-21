=====================
AVR Cross-Compilation
=====================

`Ino Tool <http://inotool.org>`_

Ino is broken !

https://github.com/amperka/ino/issues/232
https://github.com/amperka/ino/issues/228

        mcu = '-mmcu=' + 'atmega2' # Fabrice: board['build']['mcu']

https://github.com/scottdarch/Arturo

http://www.nongnu.org/avr-libc/
https://gcc.gnu.org/onlinedocs/gcc/AVR-Options.html

atmega2560 mcu type is avr6

avr-objdump -d -j .sec1 -m avr6 blink-led-mega2560-firmware.hex > blink-led-mega2560-firmware.dump
