===========
Get Started
===========

Linux
=====

This instructions are for Ubuntu 10.10 / Debian / Fedora, but it should be easy to adapt them to
other systems.

Prepare System
--------------

You need to setup your development environment, but since you are interested in an AVR simulator,
you should have done this already ;-)

* gcc
* make
* gcc-avr  
* avr-libc

Ubuntu 10.10 / Debian::

  sudo apt-get install gcc make
  sudo apt-get install gcc-avr avr-libc

To build the simulator you also need the ELF package::

  sudo apt-get install libelf-dev

And the Open GL Utility Toolkit for the GUI examples::

  sudo apt-get install freeglut3 freeglut3-dev

Fedora::

  yum install elfutils-libelf-devel gcc make avr-binutils avr-gcc avr-gdb avr-libc
     
Install simavr
--------------

1. download

   First of all you need to get the simavr sources.  direct download link:
   http://gitorious.org/simavr/simavr/archive-tarball/master
   Or clone it with GIT.

2. extract

   copy the package to your development directory and unpack it::
  
     tar xfvz simavr-simavr-master.tar.gz

3. build simavr::
  
     cd simavr-simavr
     make all

4. test your installation::
     
     make -C tests run_tests

Run Your AVR Firmware
---------------------

::

   ./simavr/run_avr firmware.afx

or::

  ./simavr/run_avr -m atmega88 - f 8000000 firmware.hex

e.g.::

  ./simavr/run_avr ./tests/atmega88_example.axf

Debug with GDB
--------------

TBD

Windows
=======

Since simavr was written for Linux it’s a bit tricky, but still possible to run it under Windows.

Prepare System
--------------

You need to setup WinAVR and Cygwin.

*WinAVR*
If you have not already, install WinAVR. (This tutorial supposes you are using WinAVR-20100110.)
http://winavr.sourceforge.net

*Cygwin*
Get setup.exe from the Cygwin homepage: (Cygwin 1.7 or later)
http://www.cygwin.com

run the setup and select the following packages:

* binutils
* gcc
* gcc-core
* gdb (optional)
* libelf0-devel
* make
* libglut-devel
* freeglut

* x-start-menue-icons (if you want to test the graphical examples)

Install simavr
--------------

1. First of all you need to get the simavr sources

   direct download link: 
   http://gitorious.org/simavr/simavr/archive-tarball/master
   and copy the package to your development directory
   Or clone it with GIT.

2. extract
   
   open the *Cygwin shell* (start Cygwin)
   Switch to the directory you have copied simavr. 
   Be aware that this is a Linux like command shell, so files are case-sensitive and there are no drive
   letters. Windows drive letters will become `/cygdrive/_driveletter_` e.g. `X: --> /cygdrive/X/...`::

     cd /cygdrive/X/my_development_directory
     tar xfvz simavr-simavr-master.tar.gz
     cd simavr-simavr

3. prepare simavr

   Open _Makefile.common_ in your simavr directory with your favorite text editor.
   Search for `AVR_ROOT := /usr/lib/avr` change this and the following lines to::
  
     AVR_ROOT := ${AVR32_HOME}
     AVR_INC := ${shell echo ${AVR32_HOME} | sed 's/\(.\):/\/cygdrive\/\1\//'}/avr
     AVR := ${AVR_ROOT}/bin/avr-
     #CFLAGS +=  -fPIC

   Search for the following block::
  
     AVR_ROOT := /usr/lib/avr
     AVR_INC := ${AVR_ROOT}
     AVR := avr-
     CFLAGS +=  -fPIC
     endif

   change it to::
  
     ifneq ($(AVR32_HOME),)
     # use WinAVR
     AVR_ROOT := ${AVR32_HOME}
     AVR_INC := ${shell echo ${AVR_ROOT} | sed 's/\(.\):/\/cygdrive\/\1\//'}/avr
     AVR := ${shell echo ${AVR_ROOT} | sed 's/\(.\):/\/cygdrive\/\1\//'}/bin/avr-
     else
     AVR_ROOT := /usr/lib/avr
     AVR_INC := ${AVR_ROOT}
     AVR := avr-
     CFLAGS +=  -fPIC
     endif
     endif

   If you have problems reading _Makefile.common_ because your editor is not able to handle UNIX texts,
   you can use `unix2dos Makefile.common` in the Cygwin shell.

   Open *tests/Makefile* and change `libsimavr.so` to `libsimavr.a` for the test_% target::

     test_%: ${OBJ}/test_%.o ${OBJ}/tests.o ${simavr}/simavr/${OBJ}/libsimavr.a

   In the header file: *simavr\sim\sim_core.h* find the declaration of `_avr_sp_get()` and add an inline::

     inline uint16_t _avr_sp_get(avr_t * avr);

   in *simavr\sim\sim_io.c* you need to add a (int) type-cast in line 199::

     while (!isalpha((int)*kind))

   Alternatively, you can download from another repository which is already "Cygwin ready", but may be
   some releases behind the main repository.
   https://gitorious.org/simavr/orcas-simavr/archive-tarball/master
   Or clone it with GIT.

4. build simavr

   Make sure that the `AVR32_HOME` environment variable is set to your WinAVR directory:
   Open a Cygwin shell and enter::

     echo $AVR32_HOME

   You should get something like::

     C:\WinAVR-20100110

   If not, set the environment Variable in your Windows settings and restart the Cygwin shell.

   Switch to the simavr directory in the *Cygwin shell*.
   Now you can build the simulator::

     make all

   If you get an error message:
   `This application has requested the Runtime to terminate in an unusual way.`
   Try to reinstall Cygwin.

5. test your installation

   in the *Cygwin shell*::
  
     cd tests
     ./run_tests
     cd ..
  
   If you get an `Permission denied` error, the executable-flag of run_tests might not be set
   correctly. Fix it with::
  
     chmod a+x run_tests

6. OpenGL – graphics with Cygwin

   Start a Cygwin X Window:
   From the Windows Start menu select: *Cygwin-X -> XWin Server*
   This may take some Section

   onds and a new *X Shell* should appear. In the Windows icon tray there is a
   new symbol: a big *X* for Cygwins X server. If no new window with an *X Shell* opens, the X
   server is probably already running: right click on the *X* in
   the *system tray -> Applications -> xterm*
   In the *X Shell* switch to the `simavr\examples\board_ledramp` directory and call::

     cd /cygdrive/X/my_development_directory
     cd simavr-simavr/examples/board_ledramp
     ./ obj-i686-pc-cygwin/ledramp.elf
     
   A new window with a LED ramp will open. Click this window do give it the focus. Now you can use the
   keys as prompted: 'SPACE', 'q', ...

Run Your AVR Firmware
---------------------

Compile your AVR program just as you would do for a real hardware (AVR Eclipse Plugin, AVR Studio, ...).
Then open a *Cygwin Shell* and run your firmware with simavr::

  ./simavr/run_avr firmware.afx

or::

  ./simavr/run_avr -m atmega88 - f 8000000 firmware.hex

e.g.::

  ./simavr/run_avr ./tests/atmega88_example.axf

Debug with GDB
--------------

TBD

Virtual PCB with simavr
=======================

One of the great thinks of simavr is, that you can build up your virtual board around the AVR.  See
the examples directory on how to build your own virtual periphery devices and how to connect them to
the AVR with IRQ callbacks.

The main interface between simavr and virtual periphery are callback functions.

avr_irq_register_notify()
-------------------------

You can register a callback function with::
  
  avr_irq_register_notify( avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ('B'), 0), my_pin_hook, my_params);

* avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ('B'), 0)
  gets the corresponding IRQ for port B pin 0
* my_pin_hook
  is the callback function that should be called when the IRQ has been triggered
* my_params
  is a pointer which is passed to the callback function, this can be a pointer to some structure or,
  using some C tweaks, an integer.

e.g.::
   
  for (i = 0; i < 8; i++)
     avr_irq_register_notify(
       avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ('B'), i), 
       pin_changed_hook, 
       (void*)i);

avr_connect_irq()
-----------------

.. End
