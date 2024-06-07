# 主编译器脚本 compiler.py

from lexer import Lexer
from yufafenxi import Parser
from jieshichengxu import Interpreter

def intermediate(old_tokens, lexer):
    type_mapping = {
        'keywords': 'RESERVE_WORD',
        'identifiers': 'IDENTIFIER',
        'punctuation': 'DELIMITER',
        'constants_int': 'CONSTANT',
        'constants_float': 'CONSTANT',
        'constants_char': 'CONSTANT',
        'constants_string': 'CONSTANT'
    }
    punctuation_mapping = {
        '(': 'DELIMITER', ')': 'DELIMITER', '{': 'DELIMITER', '}': 'DELIMITER', 
        ';': 'DELIMITER', ',': 'DELIMITER',
        '=': 'OPERATOR', '==': 'OPERATOR', '<=': 'OPERATOR', '<': 'OPERATOR', 
        '+': 'OPERATOR', '++': 'OPERATOR', '>': 'OPERATOR', '-': 'OPERATOR', 
        '*': 'OPERATOR', '/': 'OPERATOR'
    }
    new_tokens = []
    for token in old_tokens:
        token_type, index = token
        if token_type == 'punctuation':
            value = lexer.punctuation[index]
            new_type = punctuation_mapping.get(value, 'DELIMITER')
            new_tokens.append((new_type, value))
        else:
            table = getattr(lexer, token_type)
            value = table[index]
            new_type = type_mapping.get(token_type, token_type)
            new_tokens.append((new_type, value))
    return new_tokens

class Compiler:
    def __init__(self, code):
        self.code = code
        self.lexer = Lexer()#词法分析
        self.lexer.tokenize(self.code)
        self.tokens = intermediate(self.lexer.tokens, self.lexer)#生成令牌
        self.parser = Parser(self.tokens)
        self.interpreter = Interpreter(self.parser.quadruples)

    def compile(self):
        # 语法分析、语义分析、四元式生成
        print(self.tokens)
        self.parser.program()
        print(self.parser.symbol_table.table)
        print(self.parser.quadruples)
        # 解释执行
        result = self.interpreter.execute()

        return result

if __name__ == "__main__":
    with open("code1.c", "r", encoding="utf-8") as f :
        code = f.read()
    print(code)
    print()

    compiler = Compiler(code)
    result = compiler.compile()
    #展示运行结果
    for var,value in result.items():
        print(f"{var} = {value}")
