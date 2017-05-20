Tips
====

* set location of *.mmcu* without that, you get a avr-ld: section .mmcu loaded at [XXX,YYY] overlaps
  section .data loaded at [XXX,YYY]::
    
    -Wl,--undefined=_mmcu,--section-start=.mmcu=0x910000
    
* a printf-like function

  * add this function to your library::
          
      static int
      uart_putchar(char c, FILE *stream) {
        if (c == '\n')
        uart_putchar('\r', stream);
        loop_until_bit_is_set(UCSR0A, UDRE0);
        UDR0 = c;
        return 0;
      }
    
  * create a file descriptor::
      
      static FILE mystdout = FDEV_SETUP_STREAM(uart_putchar, NULL, _FDEV_SETUP_WRITE);

  * and set the file descriptor for stdout to your previous generated file descriptor::
      
      stdout = &mystdout;

.. End
