import json
import collections

from Instruction import Instruction

instructions = collections.OrderedDict()

with open('opcodes.old.json') as f:
    d = json.load(f)
    for name in sorted(d.keys()):
        description, opcodes = d[name]
        instructions[name] = Instruction(name, description, opcodes)

instructions2 = collections.OrderedDict()

with open('instruction-summary.csv') as f:
    for line in f:
        line = line.strip()
        line = line.replace('"', '')
        mnemonic, operands, description, operation, flags, cycles = line.split('|')
        if not mnemonic.startswith('#') and not mnemonic.startswith('Mnemonic'):
            if mnemonic in instructions:
                try:
                    if '/' in cycles:
                        cycles = [int(x) for x in cycles.split('/')]
                    else:
                        cycles = int(cycles)
                except ValueError:
                    cycles = cycles
                if operands:
                    operands = operands.split(", ")
                else:
                    operands = ''
                if flags == 'None':
                    flags = None
                else:
                    flags = flags.split(", ")
                instruction = instructions[mnemonic]
                instructions2[mnemonic] = instruction2 = collections.OrderedDict()
                instruction2['description'] = instruction.description
                if description != instruction.description:
                    instruction2['alternate'] = description
                instruction2['operations'] = operations = []
                for i, opcode in enumerate(instruction.opcodes):
                    opcode_dict = collections.OrderedDict()
                    operations.append(opcode_dict)
                    opcode_dict['opcode'] = opcode.opcode_string
                    if operands:
                        opcode_dict['operands'] = operands
                    opcode_dict['operation'] = operation
                    if flags is not None:
                        opcode_dict['flags'] = flags
                    opcode_dict['cycles'] = cycles
            else:
                raise NameError(mnemonic)

instructions3 = collections.OrderedDict()
for mnemonic in sorted(instructions2):
    instructions3[mnemonic] = instructions2[mnemonic]

string = json.dumps(instructions3, indent=2)

in_array = False
array_string = ''
string2 = ''
for line in string.split('\n'):
    if in_array:
        if ']' in line:
            in_array = False
            array_string = array_string.replace(',', ', ' )
            string2 += array_string + line.strip() + '\n'
        else:
            array_string += line.strip()
    elif 'flags' in line or 'operands' in line or 'cycles": [' in line:
        in_array = True
        array_string = line.rstrip()
    else:
        string2 += line + '\n'

print(string2)
