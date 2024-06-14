class Optimizer:
    def __init__(self, compiler):
        self.compiler = compiler

    def optimize(self):
        self.remove_redundant_assignments()
        self.fold_constants()
        self.remove_unused_temporaries()

    def remove_redundant_assignments(self):
        optimized_quadruples = []
        last_assignments = {}
        
        for quad in self.compiler.quadruples:
            if quad[1] == '=':
                if quad[3] in last_assignments and last_assignments[quad[3]] == quad[2]:
                    continue
                last_assignments[quad[4]] = quad[2]
            optimized_quadruples.append(quad)
        
        self.compiler.quadruples = optimized_quadruples

    def fold_constants(self):
        optimized_quadruples = []

        def is_numeric(val):
            try:
                float(val)
                return True
            except ValueError:
                return False

        for quad in self.compiler.quadruples:
            if quad[1] in ['+', '-', '*', '/']:
                if is_numeric(quad[2]):
                    left_value = float(quad[2]) if '.' in quad[2] else int(quad[2])
                else:
                    left_value = None

                if is_numeric(quad[3]):
                    right_value = float(quad[3]) if '.' in quad[3] else int(quad[3])
                else:
                    right_value = None
                
                if left_value is not None and right_value is not None:
                    if quad[1] == '+':
                        result = left_value + right_value
                    elif quad[1] == '-':
                        result = left_value - right_value
                    elif quad[1] == '*':
                        result = left_value * right_value
                    elif quad[1] == '/':
                        result = left_value / right_value
                    
                    result = str(result)
                    optimized_quadruples.append((quad[0], '=', result, None, quad[4]))
                    continue

            optimized_quadruples.append(quad)
        
        self.compiler.quadruples = optimized_quadruples

    def remove_unused_temporaries(self):
        used_temporaries = set()
        for quad in self.compiler.quadruples:
            if quad[2] and isinstance(quad[2], str) and quad[2].startswith('t'):
                used_temporaries.add(quad[2])
            if quad[3] and isinstance(quad[3], str) and quad[3].startswith('t'):
                used_temporaries.add(quad[3])
        
        optimized_quadruples = []
        for quad in self.compiler.quadruples:
            if isinstance(quad[4], str) and quad[4].startswith('t') and quad[4] not in used_temporaries:
                continue
            optimized_quadruples.append(quad)
        
        self.compiler.quadruples = optimized_quadruples

