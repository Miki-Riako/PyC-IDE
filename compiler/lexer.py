import re

class Lexer:
    def __init__(self):
        self.keywords = [
            "int",   "void", "break", "float",  "while", "do",      "struct",
            "const", "case", "for",   "return", "if",    "default", "else"
        ]
        self.punctuation = [
            "-", "/", "(", ")", "==", "<=", "<", "+",
            "*", ">", "=", ",", ";",  "++", "{", "}"
        ]
        self.re_keywords    = re.compile(r'\b(' + '|'.join(self.keywords) + r')\b')
        self.re_punctuation = re.compile(r'==|<=|>=|\+\+|[-/()<+*>=,;{}]')
        self.re_identifier  = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        self.re_float       = re.compile(r'\b\d+(\.\d+([eE][+-]?\d+)?|[eE][+-]?\d+)\b')
        self.re_decimal     = re.compile(r'\b\d+\b')
        self.re_hexadecimal = re.compile(r'\b0[xX][0-9a-fA-F]+\b')
        self.re_char        = re.compile(r"'([^'\\]|\\.)'")
        self.re_string      = re.compile(r'"((?:[^"\\]|\\.)*)"')
        self.identifiers      = []
        self.constants_int    = []
        self.constants_float  = []
        self.constants_char   = []
        self.constants_string = []
        self.tokens           = []
        self.error = False
    
    def tokenize(self, string):
        pos = 0
        while pos < len(string):
            match = self.re_keywords.match(string, pos)
            if match:
                self.tokens.append(('keywords', self.keywords.index(match.group())))
                pos = match.end()
                continue
            
            match = self.re_punctuation.match(string, pos)
            if match:
                self.tokens.append(('punctuation', self.punctuation.index(match.group())))
                pos = match.end()
                continue
            
            match = self.re_identifier.match(string, pos)
            if match:
                identifier = match.group()
                if identifier not in self.identifiers:
                    self.identifiers.append(identifier)
                self.tokens.append(('identifiers', self.identifiers.index(identifier)))
                pos = match.end()
                continue
            
            match = self.re_hexadecimal.match(string, pos)
            if match:
                hex_value = str(int(match.group(), 16))
                if hex_value not in self.constants_int:
                    self.constants_int.append(hex_value)
                self.tokens.append(('constants_int', self.constants_int.index(hex_value)))
                pos = match.end()
                continue
            
            match = self.re_float.match(string, pos)
            if match:
                float_value = match.group()
                if float_value not in self.constants_float:
                    self.constants_float.append(float_value)
                self.tokens.append(('constants_float', self.constants_float.index(float_value)))
                pos = match.end()
                continue
            
            match = self.re_decimal.match(string, pos)
            if match:
                decimal_value = match.group()
                if decimal_value not in self.constants_int:
                    self.constants_int.append(decimal_value)
                self.tokens.append(('constants_int', self.constants_int.index(decimal_value)))
                pos = match.end()
                continue
            
            match = self.re_char.match(string, pos)
            if match:
                char_value = match.group(1)
                if char_value not in self.constants_char:
                    self.constants_char.append(char_value)
                self.tokens.append(('constants_char', self.constants_char.index(char_value)))
                pos = match.end()
                continue
            
            match = self.re_string.match(string, pos)
            if match:
                string_value = match.group(1)
                if string_value not in self.constants_string:
                    self.constants_string.append(string_value)
                self.tokens.append(('constants_string', self.constants_string.index(string_value)))
                pos = match.end()
                continue
            
            if not string[pos].isspace():
                self.error = True
                return
            
            pos += 1
    
    def show(self, more_info = False):
        if (self.error):
            print("ERROR")
            return
        
        print("Token :")
        for token in self.tokens:
            if more_info:
                table = getattr(self, token[0])
                print(f"{token}: {table[token[1]]}")
            else:
                print(f"{token}")
        
        print()
        print("identifiers:"  + ', '.join(self.identifiers))
        print("constants_int:" + ', '.join(self.constants_int))
        print("constants_float:" + ', '.join(self.constants_float))
        print("constants_char:" + ', '.join(self.constants_char))
        print("constants_string:" + ', '.join(self.constants_string))

if __name__ == '__main__':
    lexer = Lexer()
    code = input()
    if code == '':
        code = 'int main() {int num; int a; num = 2; if (num > 0) {a = num; } else {a = 1; } }'
    tokens = lexer.tokenize(code)
    # tokens = lexer.tokenize(input())
    lexer.show()
