import re

class Lexer:
    def __init__(self, compiler):
        self.compiler = compiler
        self.re_keywords    = re.compile(r'\b(' + '|'.join(self.compiler.keywords) + r')\b')
        self.re_punctuation = re.compile(r'==|<=|>=|\+\+|[-/()<+*>=,;{}]')
        self.re_identifier  = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        self.re_float       = re.compile(r'\b\d+(\.\d+([eE][+-]?\d+)?|[eE][+-]?\d+)\b')
        self.re_decimal     = re.compile(r'\b\d+\b')
        self.re_hexadecimal = re.compile(r'\b0[xX][0-9a-fA-F]+\b')
        self.re_char        = re.compile(r"'([^'\\]|\\.)'")
        self.re_string      = re.compile(r'"((?:[^"\\]|\\.)*)"')
    
    def tokenize(self):
        pos = 0
        
        while pos < len(self.compiler.code):
            match = self.re_keywords.match(self.compiler.code, pos)
            if match:
                self.append_token('keywords', match.group())
                pos = match.end()
                continue
            
            match = self.re_punctuation.match(self.compiler.code, pos)
            if match:
                self.append_token('punctuation', match.group())
                pos = match.end()
                continue
            
            match = self.re_identifier.match(self.compiler.code, pos)
            if match:
                identifier = match.group()
                if identifier not in self.compiler.identifiers:
                    self.compiler.identifiers.append(identifier)
                self.append_token('identifiers', identifier)
                pos = match.end()
                continue
            
            match = self.re_hexadecimal.match(self.compiler.code, pos)
            if match:
                hex_value = str(int(match.group(), 16))
                if hex_value not in self.compiler.constants_int:
                    self.compiler.constants_int.append(hex_value)
                self.append_token('constants_int', hex_value)
                pos = match.end()
                continue
            
            match = self.re_float.match(self.compiler.code, pos)
            if match:
                float_value = match.group()
                if float_value not in self.compiler.constants_float:
                    self.compiler.constants_float.append(float_value)
                self.append_token('constants_float', float_value)
                pos = match.end()
                continue
            
            match = self.re_decimal.match(self.compiler.code, pos)
            if match:
                decimal_value = match.group()
                if decimal_value not in self.compiler.constants_int:
                    self.compiler.constants_int.append(decimal_value)
                self.append_token('constants_int', decimal_value)
                pos = match.end()
                continue
            
            match = self.re_char.match(self.compiler.code, pos)
            if match:
                char_value = match.group(1)
                if char_value not in self.compiler.constants_char:
                    self.compiler.constants_char.append(char_value)
                self.append_token('constants_char', char_value)
                pos = match.end()
                continue
            
            match = self.re_string.match(self.compiler.code, pos)
            if match:
                string_value = match.group(1)
                if string_value not in self.compiler.constants_string:
                    self.compiler.constants_string.append(string_value)
                self.append_token('constants_string', string_value)
                pos = match.end()
                continue
            
            if not self.compiler.code[pos].isspace():
                self.compiler.error = 'Invalid character: ' + self.compiler.code[pos]
                raise SyntaxError(self.compiler.error)
            
            pos += 1
    
    def append_token(self, type, val):
        self.compiler.tokens.append(self.make_token(type, val))
    
    def make_token(self, type, val):
        return (type, getattr(self.compiler, type).index(val))
