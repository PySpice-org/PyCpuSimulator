####################################################################################################

import json
import collections

####################################################################################################

instructions = collections.OrderedDict()
with open('opcodes.in.json') as f:
    for name, description, opcodes in json.load(f):
        if name in instructions or ' ' in name:
            raise
        instructions[name] = (description, opcodes)

print(json.dumps(instructions, indent=2))
