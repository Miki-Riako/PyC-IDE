class Interpreter:
    def __init__(self, compiler):
        self.compiler = compiler
        self.labels = {}

    def execute(self):
        for i, quad in enumerate(self.compiler.quadruples):
            if quad[0]:
                self.labels[quad[0]] = i

        i = 0
        while i < len(self.compiler.quadruples):
            quad = self.compiler.quadruples[i]
            op = quad[1] if len(quad) > 1 else None
            arg1 = quad[2] if len(quad) > 2 else None
            arg2 = quad[3] if len(quad) > 3 else None
            result = quad[4] if len(quad) > 4 else None

            if op == '=':
                self.compiler.variables[result] = self.compiler.variables.get(arg1, arg1)
            elif op in ['+', '-', '*', '/']:
                self.compiler.variables[result] = eval(f"{self.compiler.variables.get(arg1, arg1)} {op} {self.compiler.variables.get(arg2, arg2)}")
            elif op in ['>', '<', '==', '<=', '>=', '!=']:
                self.compiler.variables[result] = eval(f"{self.compiler.variables.get(arg1, arg1)} {op} {self.compiler.variables.get(arg2, arg2)}")
            elif op == 'jf':
                if not self.compiler.variables.get(arg1, arg1):
                    i = self.labels[result]
                    continue
            elif op == 'jmp':
                i = self.labels[result]
                continue
            elif op in ['++', '--']:
                self.compiler.variables[result] = eval(f"{self.compiler.variables.get(arg1, arg1)} {op[0]} 1")
            i += 1
