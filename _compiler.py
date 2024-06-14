from compiler import Lexer, Parser, SymbolTable, Interpreter, Optimizer, Generator

class Compiler:
    def __init__(self):
        self.keywords = [
            'int',   'void', 'break', 'float',  'while', 'do',      'struct',
            'const', 'case', 'for',   'return', 'if',    'default', 'else',
            'char', 'switch'
        ]
        self.punctuation = [
            '-', '/', '(', ')', '==', '<=', '<', '+',
            '*', '>', '=', ',', ';',  '++', '{', '}',
            '--', '.'
        ]
        self.identifiers      = []
        self.constants_int    = []
        self.constants_float  = []
        self.constants_char   = []
        self.constants_string = []
        self.tokens           = []
        self.symbol_table     = SymbolTable()
        self.quadruples       = []
        self.variables = {}
        self.code  = ''
        self.asm_code = ''
        self.error = ''
    
    def compile(self):
        lexer = Lexer(self)
        lexer.tokenize()
        parser = Parser(self)
        parser.run()
        interpret = Interpreter(self)
        interpret.execute()
        optimizer = Optimizer(self)
        optimizer.optimize()
        generator = Generator(self)
        generator.generate()
    
    def show(self, target):
        if target == 'tokens':
            for token in self.tokens:
                print(token)
        elif target == 'symbol_table':
            self.symbol_table.show()
        elif target == 'quadruples':
            for quadruple in self.quadruples:
                print(quadruple)
        elif target == 'variable':
            for var, value in self.variables.items():
                print(f"{var} = {value}")
        else:
            print('Invalid target.')
    
    def val_token(self, token):
        if token[0] == 'END':
            return 'END'
        return getattr(self, token[0])[token[1]]

if __name__ == '__main__':
    compiler = Compiler()
    # compiler.code = input()
    if compiler.code == '':
        compiler.code = '''
struct A {int n1; int n2;};
int main() {
    struct A a;
    a.n1 = 1;
    a.n2 = 2;
    return 0;
}
'''
    compiler.compile()
    compiler.show('tokens')
    compiler.show('quadruples')
    compiler.show('variable')
    # print(compiler.tokens)
    # print(compiler.quadruples)
    # print(compiler.variables)
    print('No errors found.')
