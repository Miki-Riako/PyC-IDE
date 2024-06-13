class Parser:
    def __init__(self, compiler):
        self.compiler = compiler
        self.compiler.tokens += [('END', -1)]
        self.index = 0
        self.cur = self.compiler.tokens[self.index]
        self.bracket_stack = []
        self.label_counter = 0

    def run(self):
        while self.cur and self.cur[0] != 'END':
            self.function_def()

    def cur_val(self):
        if self.cur[0] == 'END':
            return None
        else:
            return getattr(self.compiler, self.cur[0])[self.cur[1]]
    
    def is_delimiter(self):
        return self.cur_val() in [';', ',', '(', ')', '{', '}']
    
    def function_def(self):
        self.type()
        self.match_word('identifiers')
        self.match_char('(')
        self.parameter_list()
        self.match_char(')')
        self.match_char('{')
        self.code_lines()
        self.match_char('}')

    def next(self):
        self.index += 1
        if self.index < len(self.compiler.tokens):
            self.cur = self.compiler.tokens[self.index]
        else:
            self.cur = None
    
    def get_val(self, token):
        return getattr(self.compiler, token[0])[token[1]]
    
    def peek_next(self):
        if self.index + 1 < len(self.compiler.tokens):
            return self.compiler.tokens[self.index + 1]
        else:
            return None
    
    def match_word(self, type):
        if self.cur[0] == 'END':
            if self.bracket_stack:
                self.compiler.error = 'Bracket not matched!'
                raise SyntaxError(self.compiler.error)
            return
        
        if self.cur[0] != type:
            self.compiler.error = 'Expecting: ' + type + ', But got ' + self.cur_val()
            raise SyntaxError(self.compiler.error)
        
        if self.cur_val() in ['(', '{']:
            self.bracket_stack.append(self.cur_val())
        elif self.cur_val() in [')', '}']:
            if not self.bracket_stack or \
            (self.cur_val() == ')' and self.bracket_stack[-1] != '(') or \
            (self.cur_val() == '}' and self.bracket_stack[-1] != '{'):
                self.compiler.error = 'Bracket not matched!'
                raise SyntaxError(self.compiler.error)
            self.bracket_stack.pop()
        
        self.next()
    
    def match_char(self, char):
        if self.cur[0] == 'END':
            if self.bracket_stack:
                self.compiler.error = 'Bracket not matched!'
                raise SyntaxError(self.compiler.error)
            return
        
        if self.cur_val() != char:
            self.compiler.error = 'Expecting: ' + char + ', But got ' + self.cur_val()
            raise SyntaxError(self.compiler.error)
        
        if self.cur_val() in ['(', '{']:
            self.bracket_stack.append(self.cur_val())
        elif self.cur_val() in [')', '}']:
            if not self.bracket_stack or \
            (self.cur_val() == ')' and self.bracket_stack[-1] != '(') or \
            (self.cur_val() == '}' and self.bracket_stack[-1] != '{'):
                self.compiler.error = 'Bracket not matched!'
                raise SyntaxError(self.compiler.error)
            self.bracket_stack.pop()
        
        self.next()

    def match_constants(self):
        if self.cur[0] == 'END':
            if self.bracket_stack:
                self.compiler.error = 'Bracket not matched!'
                raise SyntaxError(self.compiler.error)
            return
        
        if self.cur[0] not in ['constants_int', 'constants_float', 'constants_char', 'constants_string']:
            self.compiler.error = 'Expecting: constants, But got ' + self.cur_val()
            raise SyntaxError(self.compiler.error)
        self.next()

    def match_delimiter(self):
        if self.cur[0] == 'END':
            if self.bracket_stack:
                self.compiler.error = 'Bracket not matched!'
                raise SyntaxError(self.compiler.error)
            return
        
        if not self.is_delimiter():
            self.compiler.error = 'Expecting: delimiter, But got ' + self.cur_val()
            raise SyntaxError(self.compiler.error)
        if self.cur_val() in ['(', '{']:
            self.bracket_stack.append(self.cur_val())
        elif self.cur_val() in [')', '}']:
            if not self.bracket_stack or \
            (self.cur_val() == ')' and self.bracket_stack[-1] != '(') or \
            (self.cur_val() == '}' and self.bracket_stack[-1] != '{'):
                self.compiler.error = 'Bracket not matched!'
                raise SyntaxError(self.compiler.error)
            self.bracket_stack.pop()
        
        self.next()

    def parameter_list(self):
        if self.cur and self.cur[0] == 'keywords':
            self.parameter_dec()

            while self.cur and self.is_delimiter() and self.cur_val() == ',':
                self.match_delimiter()
                self.parameter_dec()

    def parameter_dec(self):
        self.type()
        self.match_word('identifiers')

    def type(self):
        if self.cur_val() in ['int', 'float', 'char', 'void']:
            type_name = self.cur_val()
            self.match_word('keywords')
            return type_name
        else:
            self.compiler.error = 'Expecting keyword, But got ' + self.cur_val()
            raise SyntaxError(self.compiler.error)

    def code_lines(self):
        while True:
            if self.cur_val() == '}':
                break
            elif self.cur_val() in ['int', 'float', 'char', 'void']:
                self.declaration()
            else:
                self.statement()

    def declaration(self):
        var_type = self.type()
        while True:
            identifier = self.cur_val()
            self.match_word('identifiers')
            self.compiler.symbol_table.add(identifier, {'type': var_type, 'scope': 'local'})

            if self.cur_val() == ';':
                self.match_char(';')
                break
            elif self.cur_val() == ',':
                self.match_char(',')
            else:
                self.compiler.error = 'Expecting "," or ";" in declaration, But got ' + self.cur_val()
                raise SyntaxError(self.compiler.error)

    def statement(self):
        if self.cur[0] == 'identifiers':
            self.expr_statement()
        elif self.cur_val() in ['if', 'while']:
            self.control_statement()
        elif self.cur_val() == '{':
            self.match_char('{')
            self.code_lines()
            self.match_char('}')
        else:
            self.match_delimiter()

    def expr_statement(self):
        self.expr()
        if not self.is_delimiter() or self.cur_val() != ';':
            self.compiler.error = 'Missing ";"!'
            raise SyntaxError(self.compiler.error)
        self.match_delimiter()

    def control_statement(self):
        if self.cur_val() == 'if':
            self.if_statement()
        elif self.cur_val() == 'while':
            self.while_statement()
        else:
            self.compiler.error = 'Unknown control statement!'
            raise SyntaxError(self.compiler.error)

    def expr(self):
        return self.assignment_expr()

    def new_label(self):
        self.label_counter += 1
        return f'{self.label_counter}'

    def get_label(self):
        return f'{self.label_counter}'

    def assignment_expr(self):
        if self.cur[0] == 'identifiers':
            identifier = self.cur_val()
            
            if not self.compiler.symbol_table.lookup(identifier):
                self.compiler.error = 'Unknown identifier: ' + identifier
                raise SyntaxError(self.compiler.error)
            
            self.match_word('identifiers')

            if self.cur_val() in ['++', '--']:
                operator = self.cur_val()
                self.match_word('punctuation')
                quad = (self.new_label(), operator, identifier, None, identifier)
                self.compiler.quadruples.append(quad)
                return quad
            else:
                self.match_word('punctuation')
                if self.cur[0] not in ['identifiers', 'constants_int', 'constants_float', 'constants_char', 'constants_string']:
                    self.compiler.error = 'Missing the expression!'
                    raise SyntaxError(self.compiler.error)
                right_hand_side = self.add_expr()
                assign_quad = (self.new_label(), '=', right_hand_side, None, identifier)
                self.compiler.quadruples.append(assign_quad)
                return assign_quad
        else:
            self.logical_expr()

    def logical_expr(self):
        left = self.relational_expr()
        while self.cur[0] == 'punctuation' and self.cur_val() in ['!', '||', '&&']:
            operator = self.cur_val()
            self.match_word('punctuation')
            if operator == '!':
                right = None
            else:
                right = self.relational_expr()
            temp_var = self.new_temp()
            quad = (self.new_label(), operator, left, right, temp_var)
            self.compiler.quadruples.append(quad)
            left = temp_var
        return left

    def relational_expr(self):
        left = self.add_expr()
        while self.cur[0] == 'punctuation' and self.cur_val() in ['<', '>', '==', '<=', '>=', '!=']:
            operator = self.cur_val()
            self.match_word('punctuation')
            right = self.add_expr()
            temp_var = self.new_temp()
            quad = (self.new_label(), operator, left, right, temp_var)
            self.compiler.quadruples.append(quad)
            left = temp_var
        return left

    def add_expr(self):
        left = self.mul_expression()
        while self.cur[0] == 'punctuation' and self.cur_val() in ['+', '-', '++', '--']:
            operator = self.cur_val()
            self.match_word('punctuation')
            
            if operator in ['++', '--']:
                right = '1'
            else:
                if self.cur[0] not in ['identifiers', 'constants_int', 'constants_float']:
                    self.compiler.error = 'Missing the number after add or sub!'
                    raise SyntaxError(self.compiler.error)
                right = self.mul_expression()
            
            temp_var = self.new_temp()
            quad = (self.new_label(), operator, left, right, temp_var)
            self.compiler.quadruples.append(quad)
            left = temp_var
        
        return left

    def mul_expression(self):
        left = self.factor()
        
        while self.cur[0] == 'punctuation' and self.cur_val() in ['*', '/']:
            operator = self.cur_val()
            self.match_word('punctuation')
            right = self.factor()
            temp_var = self.new_temp()
            quad = (self.new_label(), operator, left, right, temp_var)
            self.compiler.quadruples.append(quad)
            left = temp_var
        
        return left

    def while_statement(self):
        self.match_char('while')
        self.match_char('(')
        condition = self.logical_expr()
        self.match_char(')')
        begin_label = self.get_label()
        start_label = self.new_label()
        self.compiler.quadruples.append((start_label, 'jf', condition, None, None))
        jump_location = len(self.compiler.quadruples) - 1
        self.match_char('{')
        self.code_lines()
        self.match_char('}')
        self.compiler.quadruples.append((self.new_label(), 'jump', None, None, begin_label))
        end_label = self.new_label()
        self.compiler.quadruples.append((end_label, None, None, None, None))
        self.compiler.quadruples[jump_location] = (start_label, 'jf', condition, None, end_label)

    def if_statement(self):
        self.match_word('keywords')
        self.match_char('(')
        condition = self.logical_expr()
        self.match_char(')')
        start_label = self.new_label()
        self.compiler.quadruples.append((start_label, 'jf', condition, None, None))
        jump_location = len(self.compiler.quadruples) - 1
        self.match_char('{')
        self.code_lines()
        self.match_char('}')
        end_label = self.new_label()
        self.compiler.quadruples.append((end_label, 'jmp', None, None, end_label))
        jump_location2 = len(self.compiler.quadruples) - 1
        void_label = self.new_label()
        self.compiler.quadruples.append((void_label, None, None, None, None))
        self.compiler.quadruples[jump_location] = (start_label, 'jf', condition, None, void_label)
        
        while self.cur and self.cur_val() in ['else']:
            self.match_word('keywords')
            
            if self.cur and self.cur_val() == 'if':
                self.if_statement()
            else:
                self.match_char('{')
                self.code_lines()
                self.match_char('}')
        
        self.compiler.quadruples[jump_location2] = (end_label, 'jmp', None, None, self.new_label())
        self.compiler.quadruples.append((self.get_label(), None, None, None, None))

    def factor(self):
        if self.cur[0] == 'punctuation' and self.cur_val() == '(':
            self.match_delimiter()
            expr_quad = self.expr()
            self.match_delimiter()
            return expr_quad
        elif self.cur[0] == 'identifiers':
            identifier = self.cur_val()
            if not self.compiler.symbol_table.lookup(identifier):
                self.compiler.error = identifier + ' is not defined!'
                raise SyntaxError(self.compiler.error)
            self.match_word('identifiers')
            return identifier
        elif self.cur[0] in ['constants_int', 'constants_float', 'constants_char', 'constants_string']:
            constants_value = self.cur_val()
            self.match_constants()
            return constants_value

    def new_temp(self):
        if not hasattr(self,'temp_count'):
            self.temp_count = 0
        temp_name = f't{self.temp_count}'
        self.temp_count += 1
        return temp_name
