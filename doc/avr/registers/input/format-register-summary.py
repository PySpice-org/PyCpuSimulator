with open('register-summary-input.txt') as f:
    fields = []
    for line in f:
        if line.startswith('(0x') or line.startswith('0x'):
            print('|'.join(fields))
            fields = []
        fields.append('"' + line.strip() + '"')

        
