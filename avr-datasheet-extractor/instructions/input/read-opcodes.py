####################################################################################################

import re
import json

####################################################################################################

instructions = []

with open('opcodes.txt') as f:
    for line in f:
        line = line.strip()
        if ' - ' in line:
            name, description = line.split(' - ')
            instructions.append([name, description, []])
        elif line:
            if ')' in line:
                line = line[line.find(') ')+2:]
            instructions[-1][2].append(line)

# for instruction in instructions:
#     print()
#     print(instruction)

print(json.dumps(instructions, indent=2))
