Search.setIndex({docnames:["api/PyCpuSimulator","api/PyCpuSimulator/Avr","api/PyCpuSimulator/Avr/HexFile","api/PyCpuSimulator/BinaryFormat","api/PyCpuSimulator/BinaryFormat/HexFile","api/PyCpuSimulator/BinaryFormat/ObjDump","api/PyCpuSimulator/Config","api/PyCpuSimulator/Config/ConfigInstall","api/PyCpuSimulator/Core","api/PyCpuSimulator/Core/Core","api/PyCpuSimulator/Core/CoreAst","api/PyCpuSimulator/Core/CoreHdlParser","api/PyCpuSimulator/Core/Instruction","api/PyCpuSimulator/Logging","api/PyCpuSimulator/Logging/Logging","api/PyCpuSimulator/Math","api/PyCpuSimulator/Math/Functions","api/PyCpuSimulator/Math/Interval","api/PyCpuSimulator/Tools","api/PyCpuSimulator/Tools/BinaryNumber","api/PyCpuSimulator/Tools/Path","api/PyCpuSimulator/Tools/RevisionVersion","api/PyCpuSimulator/Version","avr-cross-compilation","avr/atmega-640-1280-2560.register-summary","avr/index","core/alu","glossary","grammar","index","installation","instruction-set-yaml-format","reference-manual","symbols","todo"],envversion:53,filenames:["api/PyCpuSimulator.rst","api/PyCpuSimulator/Avr.rst","api/PyCpuSimulator/Avr/HexFile.rst","api/PyCpuSimulator/BinaryFormat.rst","api/PyCpuSimulator/BinaryFormat/HexFile.rst","api/PyCpuSimulator/BinaryFormat/ObjDump.rst","api/PyCpuSimulator/Config.rst","api/PyCpuSimulator/Config/ConfigInstall.rst","api/PyCpuSimulator/Core.rst","api/PyCpuSimulator/Core/Core.rst","api/PyCpuSimulator/Core/CoreAst.rst","api/PyCpuSimulator/Core/CoreHdlParser.rst","api/PyCpuSimulator/Core/Instruction.rst","api/PyCpuSimulator/Logging.rst","api/PyCpuSimulator/Logging/Logging.rst","api/PyCpuSimulator/Math.rst","api/PyCpuSimulator/Math/Functions.rst","api/PyCpuSimulator/Math/Interval.rst","api/PyCpuSimulator/Tools.rst","api/PyCpuSimulator/Tools/BinaryNumber.rst","api/PyCpuSimulator/Tools/Path.rst","api/PyCpuSimulator/Tools/RevisionVersion.rst","api/PyCpuSimulator/Version.rst","avr-cross-compilation.rst","avr/atmega-640-1280-2560.register-summary.rst","avr/index.rst","core/alu.rst","glossary.rst","grammar.rst","index.rst","installation.rst","instruction-set-yaml-format.rst","reference-manual.rst","symbols.rst","todo.rst"],objects:{"":{PyCpuSimulator:[0,0,0,"-"]},"PyCpuSimulator.Avr":{HexFile:[2,0,0,"-"],instruction_set:[1,4,1,""]},"PyCpuSimulator.Avr.HexFile":{HexFile:[2,1,1,""],HexOpcode:[2,1,1,""],HexWord:[2,1,1,""]},"PyCpuSimulator.Avr.HexFile.HexFile":{read_opcodes:[2,2,1,""]},"PyCpuSimulator.Avr.HexFile.HexOpcode":{decode:[2,2,1,""],opcode:[2,3,1,""],opcode_size:[2,3,1,""],operand_bytecode:[2,3,1,""]},"PyCpuSimulator.Avr.HexFile.HexWord":{address:[2,3,1,""],bytecode:[2,3,1,""]},"PyCpuSimulator.BinaryFormat":{HexFile:[4,0,0,"-"],ObjDump:[5,0,0,"-"]},"PyCpuSimulator.BinaryFormat.HexFile":{Chunk:[4,1,1,""],Chunks:[4,1,1,""],HexFile:[4,1,1,""]},"PyCpuSimulator.BinaryFormat.HexFile.Chunk":{address:[4,3,1,""],append:[4,2,1,""],byte_array:[4,3,1,""],data:[4,3,1,""],interval:[4,3,1,""]},"PyCpuSimulator.BinaryFormat.HexFile.Chunks":{interval:[4,3,1,""]},"PyCpuSimulator.BinaryFormat.HexFile.HexFile":{data:[4,3,1,""],iter_on_uint16:[4,2,1,""],read_uint16:[4,2,1,""],uint16_length:[4,2,1,""]},"PyCpuSimulator.BinaryFormat.ObjDump":{ObjDump:[5,1,1,""],ObjDumpLine:[5,1,1,""],ParseError:[5,5,1,""]},"PyCpuSimulator.BinaryFormat.ObjDump.ObjDumpLine":{address:[5,3,1,""],comment:[5,3,1,""],instruction_bytes:[5,3,1,""],is_word:[5,3,1,""],mnemonic:[5,3,1,""],operands:[5,3,1,""]},"PyCpuSimulator.Config":{ConfigInstall:[7,0,0,"-"]},"PyCpuSimulator.Config.ConfigInstall":{Logging:[7,1,1,""],Path:[7,1,1,""]},"PyCpuSimulator.Config.ConfigInstall.Logging":{default_config_file:[7,3,1,""],directories:[7,3,1,""],find:[7,6,1,""]},"PyCpuSimulator.Config.ConfigInstall.Path":{babel_module_directory:[7,3,1,""],config_directory:[7,3,1,""],share_directory:[7,3,1,""]},"PyCpuSimulator.Core":{Core:[9,0,0,"-"],CoreAst:[10,0,0,"-"],CoreHdlParser:[11,0,0,"-"],Instruction:[12,0,0,"-"]},"PyCpuSimulator.Core.Core":{Core:[9,1,1,""],MappedRegister:[9,1,1,""],MemoryCell:[9,1,1,""],MemoryMixin:[9,1,1,""],MemoryValueMixin:[9,1,1,""],NamedObjectMixin:[9,1,1,""],RamMemory:[9,1,1,""],Register16:[9,1,1,""],Register32:[9,1,1,""],Register64:[9,1,1,""],Register8:[9,1,1,""],Register:[9,1,1,""],RegisterFile:[9,1,1,""],RomMemory:[9,1,1,""],StandardCore:[9,1,1,""]},"PyCpuSimulator.Core.Core.Core":{check_for_register_operand:[9,2,1,""],clear_operands:[9,2,1,""],cycles:[9,3,1,""],eval_If:[9,2,1,""],eval_statement:[9,2,1,""],increment_cycle:[9,2,1,""],memory:[9,3,1,""],operands:[9,3,1,""],reset:[9,2,1,""],reset_trackers:[9,2,1,""],run_ast_program:[9,2,1,""],set_operands:[9,2,1,""],split_operand_by_type:[9,2,1,""]},"PyCpuSimulator.Core.Core.MappedRegister":{reset:[9,2,1,""],set:[9,2,1,""],str_value:[9,2,1,""]},"PyCpuSimulator.Core.Core.MemoryCell":{address:[9,3,1,""],cell_size:[9,3,1,""],memory:[9,3,1,""],set:[9,2,1,""],str_value:[9,2,1,""]},"PyCpuSimulator.Core.Core.MemoryMixin":{cell_size:[9,3,1,""],check_value:[9,2,1,""],inf:[9,3,1,""],np_dtype:[9,3,1,""],sup:[9,3,1,""],truncate:[9,2,1,""],two_complement:[9,2,1,""]},"PyCpuSimulator.Core.Core.MemoryValueMixin":{two_complement:[9,2,1,""]},"PyCpuSimulator.Core.Core.NamedObjectMixin":{name:[9,3,1,""]},"PyCpuSimulator.Core.Core.RamMemory":{reset:[9,2,1,""]},"PyCpuSimulator.Core.Core.Register":{reset:[9,2,1,""],set:[9,2,1,""],str_value:[9,2,1,""]},"PyCpuSimulator.Core.Core.RegisterFile":{cell:[9,2,1,""],dump:[9,2,1,""],reset:[9,2,1,""]},"PyCpuSimulator.Core.Core.RomMemory":{cell:[9,2,1,""],size:[9,3,1,""]},"PyCpuSimulator.Core.Core.StandardCore":{eval_Addition:[9,2,1,""],eval_Addressing:[9,2,1,""],eval_And:[9,2,1,""],eval_Assignation:[9,2,1,""],eval_Bit:[9,2,1,""],eval_BitRange:[9,2,1,""],eval_Concatenation:[9,2,1,""],eval_Constant:[9,2,1,""],eval_ConstantOperand:[9,2,1,""],eval_Division:[9,2,1,""],eval_Equal:[9,2,1,""],eval_Greater:[9,2,1,""],eval_GreaterEqual:[9,2,1,""],eval_LeftShift:[9,2,1,""],eval_Less:[9,2,1,""],eval_LessEqual:[9,2,1,""],eval_LowerNibble:[9,2,1,""],eval_Multiplication:[9,2,1,""],eval_NotEqual:[9,2,1,""],eval_Or:[9,2,1,""],eval_Register:[9,2,1,""],eval_RegisterOperand:[9,2,1,""],eval_RightShift:[9,2,1,""],eval_RotateRight:[9,2,1,""],eval_SaturatedAddition:[9,2,1,""],eval_SaturatedSubtraction:[9,2,1,""],eval_Subtraction:[9,2,1,""],eval_TwoComplement:[9,2,1,""],eval_UpperNibble:[9,2,1,""],eval_Xor:[9,2,1,""]},"PyCpuSimulator.Core.CoreAst":{Addition:[10,1,1,""],Addressing:[10,1,1,""],And:[10,1,1,""],Assignation:[10,1,1,""],BinaryExpression:[10,1,1,""],BinaryOperator:[10,1,1,""],Bit:[10,1,1,""],BitRange:[10,1,1,""],Concatenation:[10,1,1,""],Constant:[10,1,1,""],ConstantOperand:[10,1,1,""],Division:[10,1,1,""],Equal:[10,1,1,""],Expression:[10,1,1,""],Function:[10,1,1,""],Greater:[10,1,1,""],GreaterEqual:[10,1,1,""],If:[10,1,1,""],LeftShift:[10,1,1,""],Less:[10,1,1,""],LessEqual:[10,1,1,""],LowerNibble:[10,1,1,""],Multiplication:[10,1,1,""],NotEqual:[10,1,1,""],Operand:[10,1,1,""],Or:[10,1,1,""],Program:[10,1,1,""],Register:[10,1,1,""],RegisterOperand:[10,1,1,""],RightShift:[10,1,1,""],StatementList:[10,1,1,""],Subtraction:[10,1,1,""],TernaryExpression:[10,1,1,""],UnaryExpression:[10,1,1,""],UpperNibble:[10,1,1,""],Xor:[10,1,1,""]},"PyCpuSimulator.Core.CoreAst.Addressing":{memory:[10,3,1,""]},"PyCpuSimulator.Core.CoreAst.Assignation":{destination:[10,3,1,""],value:[10,3,1,""]},"PyCpuSimulator.Core.CoreAst.Expression":{iter_on_operands:[10,2,1,""],operand1:[10,3,1,""],operand2:[10,3,1,""],operand3:[10,3,1,""],operand:[10,3,1,""]},"PyCpuSimulator.Core.CoreAst.Function":{name:[10,3,1,""]},"PyCpuSimulator.Core.CoreAst.If":{condition:[10,3,1,""],else_expression:[10,3,1,""],then_expression:[10,3,1,""]},"PyCpuSimulator.Core.CoreAst.Operand":{name:[10,3,1,""]},"PyCpuSimulator.Core.CoreAst.StatementList":{add:[10,2,1,""]},"PyCpuSimulator.Core.CoreHdlParser":{Parser:[11,1,1,""],ensure_statement_list:[11,7,1,""]},"PyCpuSimulator.Core.CoreHdlParser.Parser":{p_addressing:[11,2,1,""],p_assignation:[11,2,1,""],p_binary_operation:[11,2,1,""],p_compound_statement:[11,2,1,""],p_constant_operand:[11,2,1,""],p_destination:[11,2,1,""],p_empty:[11,2,1,""],p_error:[11,2,1,""],p_expression_list:[11,2,1,""],p_expression_statement:[11,2,1,""],p_function:[11,2,1,""],p_if_statement:[11,2,1,""],p_number:[11,2,1,""],p_program:[11,2,1,""],p_register:[11,2,1,""],p_register_bit:[11,2,1,""],p_register_bit_range:[11,2,1,""],p_register_concatenation:[11,2,1,""],p_register_operand:[11,2,1,""],p_source:[11,2,1,""],p_statement:[11,2,1,""],p_statement_list:[11,2,1,""],parse:[11,2,1,""],precedence:[11,3,1,""],reserved:[11,3,1,""],start:[11,3,1,""],t_AND:[11,3,1,""],t_AT:[11,3,1,""],t_BINARY_NUMBER:[11,2,1,""],t_BIT_RANGE:[11,3,1,""],t_COLON:[11,3,1,""],t_COMMA:[11,3,1,""],t_DECIMAL_NUMBER:[11,2,1,""],t_DIVIDE:[11,3,1,""],t_DOLLAR:[11,3,1,""],t_EQUAL:[11,3,1,""],t_GREATER:[11,3,1,""],t_GREATER_EQUAL:[11,3,1,""],t_HEX_NUMBER:[11,2,1,""],t_LEFT_BRACE:[11,3,1,""],t_LEFT_BRACKET:[11,3,1,""],t_LEFT_PARENTHESIS:[11,3,1,""],t_LEFT_SHIFT:[11,3,1,""],t_LESS:[11,3,1,""],t_LESS_EQUAL:[11,3,1,""],t_MINUS:[11,3,1,""],t_NAME:[11,2,1,""],t_NOT_EQUAL:[11,3,1,""],t_OCTAL_NUMBER:[11,2,1,""],t_OR:[11,3,1,""],t_PLUS:[11,3,1,""],t_RIGHT_BRACE:[11,3,1,""],t_RIGHT_BRACKET:[11,3,1,""],t_RIGHT_PARENTHESIS:[11,3,1,""],t_RIGHT_SHIFT:[11,3,1,""],t_SEMICOLON:[11,3,1,""],t_SET:[11,3,1,""],t_TIMES:[11,3,1,""],t_XOR:[11,3,1,""],t_error:[11,2,1,""],t_ignore:[11,3,1,""],t_ignore_COMMENT:[11,3,1,""],t_newline:[11,2,1,""],test_lexer:[11,2,1,""],tokens:[11,3,1,""]},"PyCpuSimulator.Core.Instruction":{Chunk:[12,1,1,""],DecisionTree:[12,1,1,""],DecisionTreeNode:[12,1,1,""],DecodeError:[12,5,1,""],Instruction:[12,1,1,""],InstructionAlias:[12,1,1,""],InstructionBase:[12,1,1,""],InstructionSet:[12,1,1,""],Opcode:[12,1,1,""],OpcodeChunk:[12,1,1,""],OperandChunk:[12,1,1,""]},"PyCpuSimulator.Core.Instruction.Chunk":{mask:[12,3,1,""]},"PyCpuSimulator.Core.Instruction.DecisionTree":{brut_force_check:[12,2,1,""],decode:[12,2,1,""],print:[12,2,1,""]},"PyCpuSimulator.Core.Instruction.DecisionTreeNode":{decode:[12,2,1,""],print:[12,2,1,""]},"PyCpuSimulator.Core.Instruction.Instruction":{alternate:[12,3,1,""],first_opcode:[12,3,1,""],no_operand:[12,3,1,""],opcodes:[12,3,1,""],single_opcode:[12,3,1,""]},"PyCpuSimulator.Core.Instruction.InstructionAlias":{opcodes:[12,3,1,""]},"PyCpuSimulator.Core.Instruction.InstructionBase":{description:[12,3,1,""],mnemonic:[12,3,1,""]},"PyCpuSimulator.Core.Instruction.InstructionSet":{check_for_clash:[12,2,1,""],decision_tree:[12,3,1,""],iter_on_instructions:[12,2,1,""],opcode_set:[12,2,1,""],yield_bytecode:[12,2,1,""]},"PyCpuSimulator.Core.Instruction.Opcode":{cycles:[12,3,1,""],decode:[12,2,1,""],encode:[12,2,1,""],instruction:[12,3,1,""],iter_on_bytecodes:[12,2,1,""],mask:[12,3,1,""],mnemonic:[12,3,1,""],no_operand:[12,3,1,""],opcode:[12,3,1,""],opcode_intervals:[12,2,1,""],opcode_operands:[12,3,1,""],opcode_size:[12,3,1,""],opcode_string:[12,3,1,""],operand_pattern:[12,3,1,""],operation:[12,3,1,""]},"PyCpuSimulator.Core.Instruction.OpcodeChunk":{is_compatible:[12,2,1,""]},"PyCpuSimulator.Core.Instruction.OperandChunk":{decode:[12,2,1,""],encode:[12,2,1,""],is_compatible:[12,2,1,""]},"PyCpuSimulator.Logging":{Logging:[14,0,0,"-"]},"PyCpuSimulator.Logging.Logging":{setup_logging:[14,7,1,""]},"PyCpuSimulator.Math":{Functions:[16,0,0,"-"],Interval:[17,0,0,"-"]},"PyCpuSimulator.Math.Functions":{even:[16,7,1,""],middle:[16,7,1,""],odd:[16,7,1,""],rint:[16,7,1,""],sign:[16,7,1,""]},"PyCpuSimulator.Math.Interval":{Interval2D:[17,1,1,""],Interval:[17,1,1,""],IntervalInt2D:[17,1,1,""],IntervalInt:[17,1,1,""],IntervalIntSupOpen:[17,1,1,""]},"PyCpuSimulator.Math.Interval.Interval":{clone:[17,2,1,""],copy:[17,2,1,""],enlarge:[17,2,1,""],intersect:[17,2,1,""],is_empty:[17,2,1,""],is_included_in:[17,2,1,""],is_outside_of:[17,2,1,""],left_open:[17,3,1,""],length:[17,2,1,""],map_in:[17,2,1,""],map_x_in:[17,2,1,""],middle:[17,2,1,""],right_open:[17,3,1,""],unmap_x_in:[17,2,1,""],zero_length:[17,2,1,""]},"PyCpuSimulator.Math.Interval.Interval2D":{area:[17,2,1,""],bounding_box:[17,2,1,""],clone:[17,2,1,""],copy:[17,2,1,""],diagonal:[17,2,1,""],enlarge:[17,2,1,""],intersect:[17,2,1,""],is_empty:[17,2,1,""],is_included_in:[17,2,1,""],map_in:[17,2,1,""],map_xy_in:[17,2,1,""],middle:[17,2,1,""],shift:[17,2,1,""],size:[17,2,1,""],unmap_xy_in:[17,2,1,""]},"PyCpuSimulator.Math.Interval.IntervalInt":{left_open:[17,3,1,""],length:[17,2,1,""],length_float:[17,2,1,""],right_open:[17,3,1,""],to_slice:[17,2,1,""]},"PyCpuSimulator.Math.Interval.IntervalIntSupOpen":{exclude:[17,2,1,""],intersect:[17,2,1,""],minus:[17,2,1,""]},"PyCpuSimulator.Tools":{BinaryNumber:[19,0,0,"-"],Path:[20,0,0,"-"],RevisionVersion:[21,0,0,"-"]},"PyCpuSimulator.Tools.BinaryNumber":{format_as_nibble:[19,7,1,""],sup_for_nbits:[19,7,1,""]},"PyCpuSimulator.Tools.Path":{find:[20,7,1,""],find_alias:[20,7,1,""],parent_directory_of:[20,7,1,""],to_absolute_path:[20,7,1,""]},"PyCpuSimulator.Tools.RevisionVersion":{RevisionVersion:[21,1,1,""]},"PyCpuSimulator.Tools.RevisionVersion.RevisionVersion":{scale:[21,3,1,""],to_list:[21,2,1,""],version_string:[21,2,1,""]},PyCpuSimulator:{Avr:[1,0,0,"-"],BinaryFormat:[3,0,0,"-"],Config:[6,0,0,"-"],Core:[8,0,0,"-"],Logging:[13,0,0,"-"],Math:[15,0,0,"-"],Tools:[18,0,0,"-"],Version:[22,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","data","Python data"],"5":["py","exception","Python exception"],"6":["py","staticmethod","Python static method"],"7":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:data","5":"py:exception","6":"py:staticmethod","7":"py:function"},terms:{"002b":33,"00ac":33,"00b1":33,"00d7":33,"00f7":33,"00rd":31,"0x00":25,"0x0000":25,"0x01":25,"0x02":25,"0x0d":25,"0x0e":25,"0x0f":25,"0x10":25,"0x11":25,"0x1a":25,"0x1b":25,"0x1c":25,"0x1d":25,"0x1e":25,"0x1f":25,"0x1ff":25,"0x20":25,"0x200":25,"0x21ff":25,"0x2200":25,"0x2a":12,"0x3b":25,"0x3c":25,"0x3d":25,"0x3e":25,"0x3f":25,"0x5b":25,"0x5c":25,"0x5d":25,"0x5e":25,"0x5f":25,"0x60":25,"0x9000":25,"0x9200":25,"0x9408":25,"0x9409":25,"0x940c":25,"0x940e":25,"0x9418":25,"0x9419":25,"0x9428":25,"0x9438":25,"0x9448":25,"0x9458":25,"0x9468":25,"0x9478":25,"0x9488":25,"0x9498":25,"0x94a8":25,"0x94b8":25,"0x94c8":25,"0x94d8":25,"0x94e8":25,"0x94f8":25,"0x9508":25,"0x9509":25,"0x9518":25,"0x9519":25,"0x9588":25,"0x9598":25,"0x95a8":25,"0x95c8":25,"0x95d8":25,"0x95e8":25,"0x95f8":25,"0xa":12,"0xfe0e":25,"0xfe0f":25,"0xffff":25,"10a":24,"10b":24,"10c":24,"11f":24,"11rd":31,"12a":24,"12b":24,"12c":24,"12d":24,"12e":24,"12f":24,"1ff":24,"22bb":33,"22bc":33,"22c0":33,"22c1":33,"22c5":33,"279b":33,"279c":33,"279d":33,"279e":33,"27a1":33,"27f5":33,"27f6":33,"2a01":33,"2a02":33,"2b05":33,"abstract":10,"break":[1,25],"byte":[24,25],"case":25,"class":[2,4,5,7,9,10,11,12,17,21],"default":12,"float":[17,29,33],"function":[0,10,11,15,28],"long":33,"new":[12,17],"null":17,"return":[12,17],"static":7,"true":17,"try":12,AND:[1,11,31,33],And:[10,25],CLS:[1,25],For:[9,25,30],LDS:[1,25],NOT:33,SES:[1,25],STS:[1,25],The:[9,12,17,25,29,30,32],Then:30,There:25,_2q1_1q2_1d5_1q3:25,_2q1_1q2_1r5_1q3:25,_4k12:25,_4k4d4k4:25,_5a2d5a4:25,_5a2r5a4:25,_5k3d4k4:25,_6d10:25,_6k7_3:25,_6k7s3:25,_6r1d5r4:25,_7d5_1b3:25,_7d5_4:25,_7k5_3k1:25,_7r5_1b3:25,_7r5_4:25,_8a5b3:25,_8d4_4:25,_8d4r4:25,_8k2d2k4:25,_8k4_4:25,_9d3_1r3:25,_9s3_4:25,__getitem__:17,_operand:28,acbg:24,access:[17,25],acd:24,aci:24,acic:24,acis0:24,acis1:24,acm:[12,24],acmid:12,aco:24,acsr:24,actual:[25,32],adat:24,adc0d:24,adc10d:24,adc11d:24,adc12d:24,adc13d:24,adc14d:24,adc15d:24,adc1d:24,adc2d:24,adc3d:24,adc4d:24,adc5d:24,adc6d:24,adc7d:24,adc8d:24,adc9d:24,adc:[1,24,31],adch:24,adcl:24,adcsra:24,adcsrb:24,add:[1,9,10,26,28,31],addit:[10,29,30,33],addr:25,address:[2,4,5,9,10,11,12,24,28,33],aden:24,adi:24,adif:24,adiw:1,adlar:24,admux:24,adps0:24,adps1:24,adps2:24,adsc:24,adts0:24,adts1:24,adts2:24,affect:25,after:[25,29],against:34,ain0d:24,ain1d:24,algorithm:[12,26],alia:[17,31],alias_of:[12,31],alias_substitut:[12,31],all:12,allow:33,also:25,altern:[12,31],alu:[9,29],alwai:25,ambigu:33,andi:1,api:29,append:4,applic:25,application_nam:14,architectur:25,area:17,arg:[10,12,17],argument:34,ari:33,arithmet:[17,25],arrow:33,arturo:23,as2:24,ascii:29,asr:1,assembl:12,assign:[10,11,28],associ:12,assr:24,ast:34,ated:25,atmega2560:23,atmega640:25,atmel:29,attent:34,attribut:[9,17],author:12,auto:32,automat:[29,32,34],avail:30,avr6:[5,23],avr:[0,2,12,29,32],babel_module_directori:7,bad:32,base:[2,4,5,7,9,10,11,12,17,21],basic:29,baud:24,baugh:26,bcd:25,bclr:1,begin:25,between:25,binari:[12,28,29],binary_numb:[11,28],binaryexpress:10,binaryformat:[0,2,4,5,32],binarynumb:[0,18],binaryoper:10,binutil:[5,34],bird:12,bit:[9,10,24,25,26,34],bit_rang:11,bitrang:10,black:33,blbset:24,bld:[1,25],blink:23,bnf:28,booktitl:12,booth:26,borf:24,bound:17,boundari:17,bounding_box:17,box:[17,33],brb:1,brbc:1,brc:1,brcc:1,breq:1,brge:1,brh:1,brhc:1,brid:1,brie:1,brlo:1,brlt:1,brmi:1,brne:1,brpl:1,brsh:1,brt:1,brtc:1,brut_force_check:12,brv:1,brvc:1,bset:1,bst:[1,25],build:30,built:29,bullet:33,byte_arrai:4,bytecod:[2,12],calibr:24,call:[1,25,29],can:[9,12,17,25],captur:24,carri:[25,26,31],cbi:1,cbr:1,cell:9,cell_siz:9,cffi:[],cfm:12,challeng:34,check:[9,12,34],check_for_clash:12,check_for_register_operand:9,check_valu:9,chunk:[4,12],circl:33,citat:12,cite:12,clamp:17,clash:34,clc:[1,25],cleanup:25,clear:25,clear_operand:9,clh:[1,25],cli:[1,25],clkpce:24,clkpr:24,clkps0:24,clkps1:24,clkps2:24,clkps3:24,cln:[1,25],clone:[17,30],clr:1,clt:[1,25],clv:[1,25],clz:[1,25],code:[29,30,34],collect:12,colon:11,com0a0:24,com0a1:24,com0b0:24,com0b1:24,com1a0:24,com1a1:24,com1b0:24,com1b1:24,com1c0:24,com1c1:24,com2a0:24,com2a1:24,com2b0:24,com2b1:24,com3a0:24,com3a1:24,com3b0:24,com3b1:24,com3c0:24,com3c1:24,com4a0:24,com4a1:24,com4b0:24,com4b1:24,com4c0:24,com4c1:24,com5a0:24,com5a1:24,com5b0:24,com5b1:24,com5c0:24,com5c1:24,com:[1,23,29,30],comma:11,command:30,comment:[5,33],commit:29,comp:24,compar:24,compat:25,compil:29,complement:25,complet:29,compon:17,compound:33,compound_stat:[11,28],comput:17,concaten:[10,25,34],condit:10,config:[0,7,32],config_directori:7,config_fil:[7,14],configinstal:[0,6],constant:[9,10,11,28],constantoperand:10,construct:17,contain:25,content:[25,32],control:25,copi:[17,25],core:[0,10,11,12,29,32],coreast:[0,8],corehdlpars:[0,8],correspond:[12,17,34],could:[31,34],count:[12,25],counter:24,coupl:17,cpc:1,cpha:24,cpi:1,cpol:24,cpse:1,cpu:[7,29],cross:29,cs00:24,cs01:24,cs02:24,cs10:24,cs11:24,cs12:24,cs20:24,cs21:24,cs22:24,cs30:24,cs31:24,cs32:24,cs40:24,cs41:24,cs42:24,cs50:24,cs51:24,cs52:24,csv:25,cycl:[9,12,31],dadda:26,data:[4,9,24,29,34],datasheet:29,dda0:24,dda1:24,dda2:24,dda3:24,dda4:24,dda5:24,dda6:24,dda7:24,ddb0:24,ddb1:24,ddb2:24,ddb3:24,ddb4:24,ddb5:24,ddb6:24,ddb7:24,ddc0:24,ddc1:24,ddc2:24,ddc3:24,ddc4:24,ddc5:24,ddc6:24,ddc7:24,ddd0:24,ddd1:24,ddd2:24,ddd3:24,ddd4:24,ddd5:24,ddd6:24,ddd7:24,dddd:31,dde0:24,dde1:24,dde2:24,dde3:24,dde4:24,dde5:24,dde6:24,dde7:24,ddf0:24,ddf1:24,ddf2:24,ddf3:24,ddf4:24,ddf5:24,ddf6:24,ddf7:24,ddg0:24,ddg1:24,ddg2:24,ddg3:24,ddg4:24,ddg5:24,ddh0:24,ddh1:24,ddh2:24,ddh3:24,ddh4:24,ddh5:24,ddh6:24,ddh7:24,ddj0:24,ddj1:24,ddj2:24,ddj3:24,ddj4:24,ddj5:24,ddj6:24,ddj7:24,ddk0:24,ddk1:24,ddk2:24,ddk3:24,ddk4:24,ddk5:24,ddk6:24,ddk7:24,ddl0:24,ddl1:24,ddl2:24,ddl3:24,ddl4:24,ddl5:24,ddl6:24,ddl7:24,ddra:24,ddrb:24,ddrc:24,ddrd:24,ddre:24,ddrf:24,ddrg:24,ddrh:24,ddrj:24,ddrk:24,ddrl:24,deal:25,dec:1,decim:28,decimal_numb:[11,28],decis:12,decision_tre:12,decisiontre:12,decisiontreenod:12,decod:[2,12],decodeerror:12,decrement:33,default_config_fil:7,default_nod:12,defin:[9,17,25],definit:[10,11],depend:[25,29],describ:[12,29],descript:[12,31],design:34,destin:[10,11,25,28],develop:30,developp:7,devic:25,diagon:17,dictionnari:[1,12],didr0:24,didr1:24,didr2:24,directli:9,directori:[7,20],disassembl:[12,34],distribut:12,divid:11,divis:[10,33],docstr:32,document:[29,30],doe:17,doi:12,dollar:11,domain:17,don:17,done:34,dor0:24,dor1:24,dor2:24,dor3:24,dord:24,dot:33,doubl:26,draft:33,draw:33,dump:[9,23,25],each:[29,34],editor:25,eearh:24,eearl:24,eecr:24,eedr:24,eemp:24,eep:24,eepm0:24,eepm1:24,eeprom:24,eer:24,eeri:24,eical:[1,25],eicra:24,eicrb:24,eifr:24,eijmp:[1,25],eimsk:24,eind0:[24,25],eind1:25,eind2:25,eind3:25,eind4:25,eind5:25,eind6:25,eind7:25,eind:24,elpm:1,els:[11,17,28],else_express:10,empti:[11,17,28],enabl:25,encod:[12,26,31],enlarg:17,ensure_statement_list:11,eor:1,equal:[10,11,33],error:29,etc:34,eval_addit:9,eval_address:9,eval_and:9,eval_assign:9,eval_bit:9,eval_bitrang:9,eval_concaten:9,eval_const:9,eval_constantoperand:9,eval_divis:9,eval_equ:9,eval_great:9,eval_greaterequ:9,eval_if:9,eval_leftshift:9,eval_less:9,eval_lessequ:9,eval_lowernibbl:9,eval_multipl:9,eval_notequ:9,eval_or:9,eval_regist:9,eval_registeroperand:9,eval_rightshift:9,eval_rotateright:9,eval_saturatedaddit:9,eval_saturatedsubtract:9,eval_stat:9,eval_subtract:9,eval_twocompl:9,eval_uppernibbl:9,eval_xor:9,even:16,eventu:26,exampl:[9,28,31],except:[5,12],exclk:24,exclud:17,excluded_flag:17,exclus:[17,25],execut:34,expon:26,express:[10,11,28],expression_list:[11,28],expression_stat:[11,28],extend:26,extern:25,extract:29,extractor:34,extrf:24,fabric:7,fabricesalvair:[29,30],fals:[12,17],fe0:24,fe1:24,fe2:24,fe3:24,featur:29,felxibl:9,file:[1,4,9,34],file_nam:20,find:[7,20],find_alia:20,firmwar:[2,23],first:25,first_opcod:12,flag:[12,25,31],flash:25,fmul:1,fmulsu:1,foc0a:24,foc0b:24,foc1a:24,foc1b:24,foc1c:24,foc2a:24,foc2b:24,foc3a:24,foc3b:24,foc3c:24,foc4a:24,foc4b:24,foc4c:24,foc5a:24,foc5b:24,foc5c:24,follow:[25,30],form:25,format:[2,4,29],format_as_nibbl:19,fraction:26,from:[1,26,29,32],further:12,futur:25,gcc:23,gdt:12,gener:[12,24,26,32],get:17,git:[29,30],github:[23,29,30],given:[9,17],global:25,glossari:29,gnu:23,gpior0:24,gpior1:24,gpior2:24,grammar:28,greater:[10,11],greater_equ:11,greaterequ:10,group:25,gtccr:24,half:25,handl:34,hardwar:25,has:25,have:[9,12,25],hdl:[31,34],head:33,heavi:33,help:25,henrik:12,hex:[2,4,23,29],hex_numb:[11,28],hex_path:5,hexadecim:4,hexdecim:28,hexfil:[0,1,3],hexopcod:2,hexword:2,high:[10,11,24,25],home:[7,29,30],horizont:[17,33],host:30,how:[12,29],html:23,http:[4,12,23,29,30],ical:[1,25],ices1:24,ices3:24,ices4:24,ices5:24,icf1:24,icf3:24,icf4:24,icf5:24,icie1:24,icie3:24,icie4:24,icie5:24,icnc1:24,icnc3:24,icnc4:24,icnc5:24,icr1h:24,icr1l:24,icr3h:24,icr3l:24,icr4h:24,icr4l:24,icr5h:24,icr5l:24,ieee:26,if_stat:[11,28],ijmp:[1,25],implement:[9,12,17,25,29],inc:1,includ:17,increment:[28,33],increment_cycl:9,independ:25,index:[9,17,29,34],indic:[17,25],individu:25,inf:[9,17],inferior:33,initi:25,initialis:34,inproceed:12,input:24,instanc:[1,17],instruct:[0,1,5,8,27,28,29,34],instruction_byt:5,instruction_set:[1,12],instructionalia:12,instructionbas:12,instructionset:[1,12],int0:24,int1:24,int2:24,int3:24,int4:24,int5:24,int6:24,int7:24,integ:[9,17,26],intel:[2,4],intel_hex:4,inter:25,interfac:[17,24],intern:25,interrupt:25,intersect:17,interv:[0,4,15],interval2d:17,interval_refer:17,intervalint2d:17,intervalint:17,intervalintsupopen:17,intf0:24,intf1:24,intf2:24,intf3:24,intf4:24,intf5:24,intf6:24,intf7:24,is_compat:12,is_empti:17,is_included_in:17,is_outside_of:17,is_word:5,isbn:12,isc00:24,isc01:24,isc10:24,isc11:24,isc20:24,isc21:24,isc30:24,isc31:24,isc40:24,isc41:24,isc50:24,isc51:24,isc60:24,isc61:24,isc70:24,isc71:24,iter:17,iter_on_bytecod:12,iter_on_instruct:12,iter_on_operand:10,iter_on_uint16:4,ivc:24,ivsel:24,jmp:[1,25],jtd:24,jtrf:24,kei:12,know:32,kwarg:[9,10,17],languag:[10,11,29],larg:25,last:[25,30],latest:29,ldd:[1,12,25],ldi:1,led:23,left:11,left_brac:11,left_bracket:11,left_open:17,left_parenthesi:11,left_shift:11,leftshift:10,leftward:33,length:[12,17],length_float:17,less:[10,11,29],less_equ:11,lessequ:10,letter:12,level:[9,12],libc:23,libr:25,librari:32,light:33,like:25,line_numb:5,list:[4,17,31],load:[1,25],locat:[12,25,29],log:[0,7,32],logic:[25,31,33],look:12,low:[24,25],lowernibbl:10,lpm:[1,25],lsl:1,lsr:1,machin:5,made:30,manual:[25,29],map:[9,17,25,34],map_in:17,map_x_in:17,map_xy_in:17,mappedregist:9,mask:[12,25],math:[0,16,17,32],mcu:23,mcucr:24,mcusr:24,mechan:34,mega2560:23,memori:[9,10,29],memory_cel:9,memorycel:9,memorymixin:9,memoryvaluemixin:9,micro:[29,34],middl:[16,17],middlewar:12,minu:[11,17,31,33],miss:29,mixin:9,mixtur:25,mnemon:[5,12,34],mod:26,modifi:31,modul:[12,17,32],more:34,mov:1,movw:1,mpcm0:24,mpcm1:24,mpcm2:24,mpcm3:24,mstr:24,much:34,mul:[1,34],mulsu:1,multipl:[10,29,33],multipli:26,must:[12,25],mux0:24,mux1:24,mux2:24,mux3:24,mux4:24,mux5:24,name:[9,10,11,24,25,28,33,34],namedobjectmixin:9,nameerror:12,nand:33,need:[25,30,34],neg:[1,25],no_operand:12,node:12,none:[9,10,12,17,25],nongnu:23,nop:[1,25],not_equ:11,note:[12,25],notequ:10,np_dtype:9,number:[25,28,31],numpag:12,numpi:[9,29,30,32],objdump:[0,3,23],objdumplin:5,object:[2,4,5,7,9,10,11,12,17,21],occur:25,ocdr0:24,ocdr1:24,ocdr2:24,ocdr3:24,ocdr4:24,ocdr5:24,ocdr6:24,ocdr7:24,ocdr:24,ocf0a:24,ocf0b:24,ocf1a:24,ocf1b:24,ocf1c:24,ocf2a:24,ocf2b:24,ocf3a:24,ocf3b:24,ocf3c:24,ocf4a:24,ocf4b:24,ocf4c:24,ocf5a:24,ocf5b:24,ocf5c:24,ocie0a:24,ocie0b:24,ocie1a:24,ocie1b:24,ocie1c:24,ocie2a:24,ocie2b:24,ocie3a:24,ocie3b:24,ocie3c:24,ocie4a:24,ocie4b:24,ocie4c:24,ocie5a:24,ocie5b:24,ocie5c:24,ocr0a:24,ocr0b:24,ocr1ah:24,ocr1al:24,ocr1bh:24,ocr1bl:24,ocr1ch:24,ocr1cl:24,ocr2a:24,ocr2aub:24,ocr2b:24,ocr2bub:24,ocr3ah:24,ocr3al:24,ocr3bh:24,ocr3bl:24,ocr3ch:24,ocr3cl:24,ocr4ah:24,ocr4al:24,ocr4bh:24,ocr4bl:24,ocr4ch:24,ocr4cl:24,ocr5ah:24,ocr5al:24,ocr5bh:24,ocr5bl:24,ocr5ch:24,ocr5cl:24,octal_numb:[11,28],odd:16,offic:25,offici:29,one:[12,25],onli:[25,31],onlinedoc:23,opcod:[2,12,25,31,34],opcode_interv:12,opcode_operand:12,opcode_s:[2,12],opcode_set:12,opcode_str:12,opcodechunk:12,oper:[9,12,25,31,33,34],operand1:[9,10],operand2:[9,10],operand3:[9,10],operand:[5,9,10,12,25,27,28,31,34],operand_bytecod:2,operand_pattern:12,operandchunk:12,opposit:29,optim:12,option:[23,31],ordereddict:12,org:[4,12,23,29,30],ori:1,osccal:24,oscil:24,other:12,out:[1,24,25],output:[5,24],outsid:17,overflow:25,p100:24,p110:24,p111:24,p112:24,p113:24,p114:24,p126:24,p129:24,p130:24,p131:24,p13:24,p154:24,p156:24,p157:24,p158:24,p159:24,p15:24,p160:24,p161:24,p162:24,p166:24,p16:24,p179:24,p185:24,p186:24,p188:24,p197:24,p198:24,p199:24,p218:24,p222:24,p233:24,p234:24,p235:24,p261:24,p262:24,p263:24,p264:24,p266:24,p267:24,p281:24,p285:24,p286:24,p287:24,p288:24,p294:24,p301:24,p323:24,p34:24,p36:24,p38:24,p48:24,p50:24,p55:24,p56:24,p64:24,p65:24,p96:24,p97:24,p98:24,p99:24,p_address:11,p_assign:11,p_binary_oper:11,p_compound_stat:11,p_constant_operand:11,p_destin:11,p_empti:11,p_error:11,p_expression_list:11,p_expression_stat:11,p_function:11,p_if_stat:11,p_number:11,p_program:11,p_regist:11,p_register_bit:11,p_register_bit_rang:11,p_register_concaten:11,p_register_operand:11,p_sourc:11,p_statement:11,p_statement_list:11,page:[12,24,29,30,32],pair:12,paper:12,paramet:17,parent_directory_of:20,pars:[5,11],parseerror:5,parser:11,part:25,partial:34,particular:12,pass:12,path:[0,2,4,7,18],pattern:25,pcicr:24,pcie0:24,pcie1:24,pcie2:24,pcif0:24,pcif1:24,pcif2:24,pcifr:24,pcint0:24,pcint10:24,pcint11:24,pcint12:24,pcint13:24,pcint14:24,pcint15:24,pcint16:24,pcint17:24,pcint18:24,pcint19:24,pcint1:24,pcint20:24,pcint21:24,pcint22:24,pcint23:24,pcint2:24,pcint3:24,pcint4:24,pcint5:24,pcint6:24,pcint7:24,pcint8:24,pcint9:24,pcmsk0:24,pcmsk1:24,pcmsk2:24,pdf:25,pdftotext:25,perfect:32,perform:[9,25],peripher:[25,34],pger:24,pgwrt:24,pinb0:24,pinb1:24,pinb2:24,pinb3:24,pinb4:24,pinb5:24,pinb6:24,pinb7:24,pinb:24,pinc0:24,pinc1:24,pinc2:24,pinc3:24,pinc4:24,pinc5:24,pinc6:24,pinc7:24,pinc:24,pind0:24,pind1:24,pind2:24,pind3:24,pind4:24,pind5:24,pind6:24,pind7:24,pind:24,pine0:24,pine1:24,pine2:24,pine3:24,pine4:24,pine5:24,pine6:24,pine7:24,pine:24,pinf0:24,pinf1:24,pinf2:24,pinf3:24,pinf4:24,pinf5:24,pinf6:24,pinf7:24,pinf:24,ping0:24,ping1:24,ping2:24,ping3:24,ping4:24,ping5:24,ping:24,pinh0:24,pinh1:24,pinh2:24,pinh3:24,pinh4:24,pinh5:24,pinh6:24,pinh7:24,pinh:24,pinj0:24,pinj1:24,pinj2:24,pinj3:24,pinj4:24,pinj5:24,pinj6:24,pinj7:24,pinj:24,pink0:24,pink1:24,pink2:24,pink3:24,pink4:24,pink5:24,pink6:24,pink7:24,pink:24,pinl0:24,pinl1:24,pinl2:24,pinl3:24,pinl4:24,pinl5:24,pinl6:24,pinl7:24,pinl:24,pip:30,plu:[11,33],plug:34,point:[29,33],pop:1,porf:24,port:24,porta0:24,porta1:24,porta2:24,porta3:24,porta4:24,porta5:24,porta6:24,porta7:24,porta:24,portb0:24,portb1:24,portb2:24,portb3:24,portb4:24,portb5:24,portb6:24,portb7:24,portb:24,portc0:24,portc1:24,portc2:24,portc3:24,portc4:24,portc5:24,portc6:24,portc7:24,portc:24,portd0:24,portd1:24,portd2:24,portd3:24,portd4:24,portd5:24,portd6:24,portd7:24,portd:24,porte0:24,porte1:24,porte2:24,porte3:24,porte4:24,porte5:24,porte6:24,porte7:24,portf0:24,portf1:24,portf2:24,portf3:24,portf4:24,portf5:24,portf6:24,portf7:24,portf:24,portg0:24,portg1:24,portg2:24,portg3:24,portg4:24,portg5:24,portg:24,porth0:24,porth1:24,porth2:24,porth3:24,porth4:24,porth5:24,porth6:24,porth7:24,porth:24,portj0:24,portj1:24,portj2:24,portj3:24,portj4:24,portj5:24,portj6:24,portj7:24,portj:24,portk0:24,portk1:24,portk2:24,portk3:24,portk4:24,portk5:24,portk6:24,portk7:24,portk:24,portl0:24,portl1:24,portl2:24,portl3:24,portl4:24,portl5:24,portl6:24,portl7:24,portl:24,possibl:25,power:25,pradc:24,preced:11,precis:26,present:25,previou:26,print:12,procedur:29,proceed:12,produc:32,program:[9,10,11,25,28,34],prone:29,properti:9,provid:1,prr0:24,prr1:24,prspi:24,prtim0:24,prtim1:24,prtim2:24,prtim3:24,prtim4:24,prtim5:24,prtwi:24,prusart0:24,prusart1:24,prusart2:24,prusart3:24,psrasi:24,psrsync:24,publish:12,pud:24,purpos:24,push:1,pycpusimul:[1,2,4,5,7,9,10,11,12,14,16,17,19,20,21,29,30,32],pypi:[29,32],pyspic:[29,30],python:[7,9,29,30,32],r13:25,r14:25,r15:25,r16:25,r17:25,r26:25,r27:25,r28:25,r29:25,r30:25,r31:25,ram:9,rammemori:9,rampz0:[24,25],rampz1:[24,25],rampz2:25,rampz3:25,rampz4:25,rampz5:25,rampz6:25,rampz7:25,rampz:24,rang:9,rate:24,rcall:1,rd3:31,rd7:31,read:[2,4,25,29,34],read_opcod:2,read_uint16:4,readthedoc:[29,30],refer:[12,26],reformat:25,refs0:24,refs1:24,regist:[9,10,11,28,29,31,34],register16:9,register32:9,register64:9,register8:9,register_bit:[11,28],register_bit_rang:[11,28],register_concaten:[11,28],registerfil:9,registeroperand:10,rel:28,releas:30,repositori:29,requir:30,reserv:[11,24,25],reset:9,reset_track:9,respect:17,result:[12,25],ret:[1,25],reti:[1,25],revisionvers:[0,18],right_brac:11,right_bracket:11,right_open:17,right_parenthesi:11,right_shift:11,rightshift:10,rightward:33,rint:16,rjmp:1,rol:1,rom:[9,34],rommemori:9,ror:1,round:33,routin:[25,34],rr3:31,rr7:31,rrrr:31,run:[30,34],run_ast_program:9,rupt:25,rwwsb:24,rwwsre:24,rxb80:24,rxb81:24,rxb82:24,rxb83:24,rxc0:24,rxc1:24,rxc2:24,rxc3:24,rxcie0:24,rxcie1:24,rxcie2:24,rxcie3:24,rxen0:24,rxen1:24,rxen2:24,rxen3:24,sbc:1,sbci:1,sbi:1,sbic:1,sbiw:1,sbr:1,sbrc:1,scale:21,scottdarch:23,script:25,search:32,sec1:23,sec:[1,25],second:[25,26],section:34,see:[4,12,34],seh:[1,25],sei:[1,25],semicolon:11,sen:[1,25],separ:[25,33],ser:1,seri:12,serial:24,set:[1,9,11,12,17,25,29,34],set_operand:9,setup:30,setup_log:14,sev:[1,25],sever:12,sez:[1,25],share:7,share_directori:7,shift:17,show:12,sign:[16,25,26,33],sigplan:12,sigrd:24,simul:[7,29],single_opcod:12,size:[9,17],slash:33,sleep:[1,25],slice:17,sm0:24,sm1:24,sm2:24,small:25,smcr:24,snippet:12,snow:12,some:25,sourc:[2,4,5,7,9,10,11,12,14,16,17,19,20,21,25,29,32],sp0:[24,25],sp10:[24,25],sp11:[24,25],sp12:[24,25],sp13:[24,25],sp14:[24,25],sp15:[24,25],sp1:[24,25],sp2:[24,25],sp3:[24,25],sp4:[24,25],sp5:[24,25],sp6:[24,25],sp7:[24,25],sp8:[24,25],sp9:[24,25],space:25,spcr:24,spdr:24,spe:24,specif:4,sph:[24,25,34],sphinx:[29,30,32],spi2x:24,spi:24,spie:24,spif:24,spl:[24,25,34],split_operand_by_typ:9,spm:1,spmcsr:24,spmen:24,spmie:24,spr0:24,spr1:24,spreadsheet:25,spsr:24,sram:25,sre:24,sreg:[24,34],srl0:24,srl1:24,srl2:24,srw00:24,srw01:24,srw10:24,srw11:24,stage:26,standard:9,standardcor:9,start:11,statement:[9,10,11,27,28,33],statement_list:[11,28],statementlist:10,std:[1,25],step:20,storag:25,store:[12,25],str_valu:9,structur:25,sub:1,subi:1,subroutin:25,subsequ:25,subset:[17,34],substitut:[26,31,34],subtract:[10,25,29,33],sum:26,summari:29,sup:[9,17],sup_for_nbit:19,superior:33,support:[17,25,29],sure:25,swap:1,symbol:29,syntact:10,system:12,t_and:11,t_at:11,t_binary_numb:11,t_bit_rang:11,t_colon:11,t_comma:11,t_decimal_numb:11,t_divid:11,t_dollar:11,t_equal:11,t_error:11,t_greater:11,t_greater_equ:11,t_hex_numb:11,t_ignor:11,t_ignore_com:11,t_left_brac:11,t_left_bracket:11,t_left_parenthesi:11,t_left_shift:11,t_less:11,t_less_equ:11,t_minu:11,t_name:11,t_newlin:11,t_not_equ:11,t_octal_numb:11,t_or:11,t_plu:11,t_right_brac:11,t_right_bracket:11,t_right_parenthesi:11,t_right_shift:11,t_semicolon:11,t_set:11,t_time:11,t_xor:11,tabl:[25,26],tccr0a:24,tccr0b:24,tccr1a:24,tccr1b:24,tccr1c:24,tccr2a:24,tccr2b:24,tccr3a:24,tccr3b:24,tccr3c:24,tccr4a:24,tccr4b:24,tccr4c:24,tccr5a:24,tccr5b:24,tccr5c:24,tcn2ub:24,tcnt0:24,tcnt1h:24,tcnt1l:24,tcnt2:24,tcnt3h:24,tcnt3l:24,tcnt4h:24,tcnt4l:24,tcnt5h:24,tcnt5l:24,tcr2aub:24,tcr2bub:24,termin:30,ternaryexpress:10,test:[12,17,31,34],test_lex:11,text:[11,25,31],theil:12,then_express:10,thi:[9,12,17,25,30,32],three:25,thu:[29,34],tifr0:24,tifr1:24,tifr2:24,tifr3:24,tifr4:24,tifr5:24,time:[11,33],timer:24,timsk0:24,timsk1:24,timsk2:24,timsk3:24,timsk4:24,timsk5:24,tip:33,titl:12,to_absolute_path:20,to_list:21,to_slic:17,todo:29,toie0:24,toie1:24,toie2:24,toie3:24,toie4:24,toie5:24,token:11,too:32,tool:[0,19,20,21,25,32],tov0:24,tov1:24,tov2:24,tov3:24,tov4:24,tov5:24,translat:34,tree:[10,12,26],triangl:33,truncat:9,truth:26,tsm:24,tst:[1,31],twa0:24,twa1:24,twa2:24,twa3:24,twa4:24,twa5:24,twa6:24,twam0:24,twam1:24,twam2:24,twam3:24,twam4:24,twam5:24,twam6:24,twamr:24,twar:24,twbr:24,twcr:24,twdr:24,twea:24,twen:24,twgce:24,twie:24,twint:24,two:[9,17,25,26,31],two_compl:9,twps0:24,twps1:24,tws3:24,tws4:24,tws5:24,tws6:24,tws7:24,twsr:24,twsta:24,twsto:24,twwc:24,txb80:24,txb81:24,txb82:24,txb83:24,txc0:24,txc1:24,txc2:24,txc3:24,txcie0:24,txcie1:24,txcie2:24,txcie3:24,txen0:24,txen1:24,txen2:24,txen3:24,type:[9,23],u2x0:24,u2x1:24,u2x2:24,u2x3:24,ubrr0h:24,ubrr0l:24,ubrr1h:24,ubrr1l:24,ubrr2h:24,ubrr2l:24,ubrr3h:24,ubrr3l:24,ucpol0:24,ucpol1:24,ucpol2:24,ucpol3:24,ucsr0a:24,ucsr0b:24,ucsr0c:24,ucsr1a:24,ucsr1b:24,ucsr1c:24,ucsr2a:24,ucsr2b:24,ucsr2c:24,ucsr3a:24,ucsr3b:24,ucsr3c:24,ucsz00:24,ucsz01:24,ucsz02:24,ucsz10:24,ucsz11:24,ucsz12:24,ucsz20:24,ucsz21:24,ucsz22:24,ucsz30:24,ucsz31:24,ucsz32:24,udr0:24,udr1:24,udr2:24,udr3:24,udre0:24,udre1:24,udre2:24,udre3:24,udrie0:24,udrie1:24,udrie2:24,udrie3:24,uint16_length:4,umsel00:24,umsel01:24,umsel10:24,umsel11:24,umsel20:24,umsel21:24,umsel30:24,umsel31:24,unaryexpress:10,unicod:29,union:17,unit:25,unmap_x_in:17,unmap_xy_in:17,unus:25,upe0:24,upe1:24,upe2:24,upe3:24,upm00:24,upm01:24,upm10:24,upm11:24,upm20:24,upm21:24,upm30:24,upm31:24,uppernibbl:10,url:12,usa:12,usart0:24,usart1:24,usart2:24,usart3:24,usbs0:24,usbs1:24,usbs2:24,usbs3:24,use:[17,25,34],used:25,useful:25,uses:26,using:[9,17,25,32],utah:12,valid:34,valu:[9,10,12,17,25],verbos:12,veri:9,version:[0,21,32],version_str:21,versu:34,vertic:17,viewer:25,volatil:25,wai:32,wallac:26,wcol:24,wdce:24,wde:24,wdie:24,wdif:24,wdp0:24,wdp1:24,wdp2:24,wdp3:24,wdr:[1,25],wdrf:24,wdtcsr:24,welcom:29,wgm00:24,wgm01:24,wgm02:24,wgm10:24,wgm11:24,wgm12:24,wgm13:24,wgm20:24,wgm21:24,wgm22:24,wgm30:24,wgm31:24,wgm32:24,wgm33:24,wgm40:24,wgm41:24,wgm42:24,wgm43:24,wgm50:24,wgm51:24,wgm52:24,wgm53:24,where:17,whether:17,which:[25,31],wide:33,wiki:4,wikipedia:4,wire:24,without:25,woolei:26,word:34,workshop:12,wrapper:9,write:25,www:23,xmbk:24,xmcra:24,xmcrb:24,xmm0:24,xmm1:24,xmm2:24,xor:[10,11,26,33],yaml:[1,29,34],yaml_path:12,year:12,yield_bytecod:12,yml:[7,14],york:12,you:[29,30],z_0:[11,28],zero:[25,31],zero_length:17},titles:["6.1. PyCpuSimulator","6.1.1. Avr","6.1.1.1. HexFile","6.1.2. BinaryFormat","6.1.2.1. HexFile","6.1.2.2. ObjDump","6.1.3. Config","6.1.3.1. ConfigInstall","6.1.4. Core","6.1.4.1. Core","6.1.4.2. CoreAst","6.1.4.3. CoreHdlParser","6.1.4.4. Instruction","6.1.5. Logging","6.1.5.1. Logging","6.1.6. Math","6.1.6.1. Functions","6.1.6.2. Interval","6.1.7. Tools","6.1.7.1. BinaryNumber","6.1.7.2. Path","6.1.7.3. RevisionVersion","6.1.8. Version","11. AVR Cross-Compilation","2.1. ATmega640/1280/1281/2560/2561 Register Summary","2. AVR Datasheet","9. ALU","5. Glossary","3. Micro Code Language","Introduction","1. Installation","4. Instruction Set YAML Format","6. API Documentation","7. ASCII symbols","10. Todo"],titleterms:{"float":26,"function":16,adder:26,addit:26,alu:26,api:32,ascii:33,atmega640:24,atmel:25,avr:[1,23,25,34],basic:34,binari:26,binaryformat:3,binarynumb:19,code:28,compil:23,complet:34,config:6,configinstal:7,core:[8,9,34],coreast:10,corehdlpars:11,cpu:34,cross:23,data:25,datasheet:25,decis:[],depend:30,document:32,eind:25,elpm:25,extend:25,extract:25,featur:34,file:25,format:31,from:[25,30],full:26,gener:25,glossari:27,half:26,hex:34,hexfil:[2,4],how:[25,34],implement:34,index:32,indirect:25,instal:[29,30],instruct:[12,25,31],interv:17,introduct:29,languag:28,log:[13,14],math:15,memori:25,micro:28,miss:34,multipl:26,objdump:5,opcod:[],overview:29,path:20,point:26,pointer:25,purpos:25,pycpusimul:0,pypi:30,rampz:25,regist:[24,25],repositori:30,revisionvers:21,set:31,simul:34,sourc:30,spm:25,sreg:25,stack:25,statu:25,subtract:26,summari:[24,25],support:34,symbol:33,todo:34,tool:18,tree:[],unicod:33,version:22,yaml:31}})