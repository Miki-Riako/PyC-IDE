class Generator:
    def __init__(self, compiler):
        self.compiler = compiler
        self.asm_code = []
        self.label_counter = 0
        self.temp_count = 0

    def generate(self):
        for quad in self.compiler.quadruples:
            label, op, arg1, arg2, result = quad

            if label:
                self.asm_code.append(f"{label}:")

            if op == '=':
                self.asm_code.append(f"    MOV {result}, {arg1}")
            elif op in ['+', '-', '*', '/']:
                self.generate_arithmetic(op, arg1, arg2, result)
            elif op in ['>', '<', '==', '<=', '>=', '!=']:
                self.generate_comparison(op, arg1, arg2, result)
            elif op == 'jf':
                self.asm_code.append(f"    CMP {arg1}, 0")
                self.asm_code.append(f"    JE {result}")
            elif op == 'jmp':
                self.asm_code.append(f"    JMP {result}")
            elif op == '++':
                self.asm_code.append(f"    INC {arg1}")
            elif op == '--':
                self.asm_code.append(f"    DEC {arg1}")
            elif op == 'param':
                self.generate_param(arg1)
            elif op == 'call':
                self.generate_call(arg1, result)
            elif op == 'return':
                self.generate_return(arg1)

        self.compiler.asm_code = "\n".join(self.asm_code)

    def generate_arithmetic(self, op, arg1, arg2, result):
        self.asm_code.append(f"    MOV AX, {arg1}")
        if op == '+':
            self.asm_code.append(f"    ADD AX, {arg2}")
        elif op == '-':
            self.asm_code.append(f"    SUB AX, {arg2}")
        elif op == '*':
            self.asm_code.append(f"    MUL {arg2}")  # MUL in x86 implicitly uses AX
        elif op == '/':
            self.asm_code.append(f"    MOV DX, 0")  # Clear DX for DIV operation
            self.asm_code.append(f"    DIV {arg2}")  # DIV in x86 implicitly uses AX and DX
        self.asm_code.append(f"    MOV {result}, AX")

    def generate_comparison(self, op, arg1, arg2, result):
        self.asm_code.append(f"    MOV AX, {arg1}")
        self.asm_code.append(f"    CMP AX, {arg2}")
        if op == '>':
            self.asm_code.append(f"    JG {result}")
        elif op == '<':
            self.asm_code.append(f"    JL {result}")
        elif op == '==':
            self.asm_code.append(f"    JE {result}")
        elif op == '>=':
            self.asm_code.append(f"    JGE {result}")
        elif op == '<=':
            self.asm_code.append(f"    JLE {result}")
        elif op == '!=':
            self.asm_code.append(f"    JNE {result}")

    def generate_param(self, arg):
        self.asm_code.append(f"    PUSH {arg}")

    def generate_call(self, function_name, result):
        self.asm_code.append(f"    CALL {function_name}")
        self.asm_code.append(f"    MOV {result}, AX")

    def generate_return(self, arg):
        if arg:
            self.asm_code.append(f"    MOV AX, {arg}")
        self.asm_code.append(f"    RET")

    def new_temp(self):
        self.temp_count += 1
        return f'temp{self.temp_count}'
