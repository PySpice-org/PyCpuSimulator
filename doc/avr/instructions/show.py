####################################################################################################

from Instruction import instructions, DecisionTree

####################################################################################################
        
# for instruction in instructions.values():
#     print()
#     print(instruction.mnemonic)
#     for i, opcode in enumerate(instruction.opcodes):
#         print("  {:2} 0x{:04x} 0x{:04x} | {} | {}".format(i,
#                                                           opcode.opcode, opcode.mask,
#                                                           opcode.opcode_string,
#                                                           opcode.operand_pattern))

# print("\nMulti-Opcodes Instructions:")
# for instruction in instructions.values():
#     if not instruction.single_opcode:
#         print(' ', instruction.mnemonic)

# print("\n32-bit Opcodes:")
# for instruction in instructions.values():
#     for opcode in instruction.opcodes:
#         if opcode.opcode_size == 32:
#             print('  {:6s} 0x{:04x} 0x{:04x}'.format(instruction.mnemonic, opcode.opcode, opcode.mask))
        
# print("\nOpcodes without operand:")
# for instruction in instructions.values():
#     # if instruction.no_operand:
#     for opcode in instruction.opcodes:
#         if opcode.no_operand:
#             print('  {:6s} 0x{:04x}'.format(instruction.mnemonic, opcode.opcode))
            
# print("\nOperand patterns:")
# operand_patterns = {}
# for instruction in instructions.values():
#     for opcode in instruction.opcodes:
#         if opcode.no_operand:
#             continue
#         if opcode.operand_pattern in operand_patterns:
#             operand_patterns[opcode.operand_pattern] += 1
#         else:
#             operand_patterns[opcode.operand_pattern] = 1
# for operand_pattern in sorted(operand_patterns):
#     print('  {:16} {:3}'.format(operand_pattern, operand_patterns[operand_pattern]))

print("\nOpcodes:")
opcodes = []
for instruction in instructions.values():
    for opcode in instruction.opcodes:
        opcodes.append(opcode)
for opcode in sorted(opcodes, key=lambda x: x.opcode):
    print('  0x{:04x} 0x{:04x} {}'.format(opcode.opcode, opcode.mask, opcode.instruction.mnemonic))

# decision_tree = DecisionTree(instructions)
# print("\nMasks:")
# decision_tree.print_masks()
# print("\nDecision Tree:")
# decision_tree.print_tree()

####################################################################################################
# 
# End
# 
####################################################################################################
