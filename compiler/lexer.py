import re

class Lexer:
    def __init__(self, compiler):
        self.compiler = compiler
        self.re_keywords    = re.compile(r'\b(' + '|'.join(self.compiler.keywords) + r')\b')
        self.re_punctuation = re.compile(r'==|<=|>=|\+\+|--|[-/()<+*>=,;{}\.]')
        self.re_identifier  = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        self.re_float       = re.compile(r'-?\b\d+(\.\d+([eE][+-]?\d+)?|[eE][+-]?\d+)\b')
        self.re_decimal     = re.compile(r'-?\b\d+\b')
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
        
        self.post_process_tokens()
    
    def append_token(self, type, val):
        self.compiler.tokens.append(self.make_token(type, val))
    
    def make_token(self, type, val):
        return (type, getattr(self.compiler, type).index(val))

    def post_process_tokens(self):
        processed_tokens = []
        i = 0
        
        while i < len(self.compiler.tokens):
            token = self.compiler.tokens[i]
            
            if token[0] == 'punctuation' and self.compiler.punctuation[token[1]] == '-':
                if i > 0 and self.compiler.tokens[i-1][0] in ['punctuation', 'keywords'] and self.compiler.tokens[i-1][1] != self.compiler.punctuation.index(')'):
                    if i < len(self.compiler.tokens) - 1 and self.compiler.tokens[i+1][0] in ['constants_int', 'constants_float']:
                        next_token = self.compiler.tokens[i+1]
                        if next_token[0] == 'constants_int':
                            new_val = '-' + self.compiler.constants_int[next_token[1]]
                            self.compiler.constants_int[next_token[1]] = new_val
                        elif next_token[0] == 'constants_float':
                            new_val = '-' + self.compiler.constants_float[next_token[1]]
                            self.compiler.constants_float[next_token[1]] = new_val
                        
                        new_type = next_token[0]
                        self.compiler.tokens.pop(i+1)
                        processed_tokens.append(self.make_token(new_type, new_val))
                        i += 1
                        continue
            
            processed_tokens.append(token)
            i += 1
        
        self.compiler.tokens = processed_tokens
