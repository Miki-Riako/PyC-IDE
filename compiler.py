from compiler.lexer import Lexer
from compiler._parser import Parser
from compiler.symbol_table import SymbolTable

class Compiler:
    def __init__(self):
        self.keywords = [
            'int',   'void', 'break', 'float',  'while', 'do',      'struct',
            'const', 'case', 'for',   'return', 'if',    'default', 'else',
            'char'
        ]
        self.punctuation = [
            '-', '/', '(', ')', '==', '<=', '<', '+',
            '*', '>', '=', ',', ';',  '++', '{', '}'
        ]
        self.identifiers      = []
        self.constants_int    = []
        self.constants_float  = []
        self.constants_char   = []
        self.constants_string = []
        self.tokens           = []
        self.symbol_table     = SymbolTable()
        self.quadruples       = []
        self.code  = ''
        self.error = ''
    
    def compile(self):
        lexer = Lexer(self)
        lexer.tokenize()
        parser = Parser(self)
        parser.run()
        # interpret = Interpreter(self)
        # interpret.execute()
    
    def show(self, target):
        if (target == 'tokens'):
            for token in self.tokens:
                print(token)
        elif (target == 'symbol_table'):
            self.symbol_table.show()
        elif (target == 'quadruples'):
            for quadruple in self.quadruples:
                print(quadruple)
        else:
            print('Invalid target.')
    
    def val_token(self, token):
        return getattr(self, token[0])[token[1]]

if __name__ == '__main__':
    compiler = Compiler()
    # compiler.code = input()
    if compiler.code == '':
        compiler.code = 'int main() { int num; int a; num = 2; if (num > 0) { a = num; } else { a = 1; } }'

    compiler.compile()
    compiler.show('tokens')
    compiler.show('quadruples')
    print('No errors found.')
