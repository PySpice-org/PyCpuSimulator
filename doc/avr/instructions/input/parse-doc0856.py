####################################################################################################

import re

####################################################################################################

instruction_regexp = "^[A-Z]+.* – [A-Z]"
instruction_re = re.compile(instruction_regexp)

page_number = 0
in_opcode = False
opcode = []

with open('doc0856.txt') as f:
    for line in f:
        line = line.strip()
        if '0856I–AVR–07/10' in line:
            page_number += 1
            # print('Page', page_number)
        elif instruction_re.match(line):
            print()
            print(line)
        elif line[3:].startswith('bit Opcode:'):
            in_opcode = True
            opcode = []
        elif re.match('^[A-Z][a-z]+( |:)', line):
            if opcode:
                print(' '.join(opcode))
            in_opcode = False
            opcode = []
        else:
            if in_opcode and line:
                if line.startswith('('):
                    if opcode:
                        print(' '.join(opcode))
                    opcode = [line]
                else:
                    opcode.append(line)
