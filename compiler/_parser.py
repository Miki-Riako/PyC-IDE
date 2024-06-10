class Parser:
    def __init__(self, compiler):
        self.compiler = compiler
        self.compiler.tokens += [('END', -1)]
        self.index = 0
        self.cur = self.compiler.tokens[self.index]
        self.bracket_stack = []
        self.label_counter = 0

    def run(self):
        while (self.cur and self.cur[0] != 'END'):
            self.function_def()

    def cur_val(self):
        return getattr(self.compiler, self.cur[0])[self.cur[1]]
    
    def is_delimiter(self):
        return self.cur_val() in [';', ',', '(', ')', '{', '}']
    
    def function_def(self):
        self.type()
        self.match_word('identifiers')
        self.match_delimiter()
        self.parameter_list()
        self.match_delimiter()
        self.compound_statement()

    def next(self):
        self.index += 1
        if self.index < len(self.compiler.tokens):
            self.cur = self.compiler.tokens[self.index]
        else:
            self.cur = None
    
    def match_word(self, type):
        if self.cur[0] == 'END':
            if self.bracket_stack:
                raise SyntaxError('Bracket no matched!')
            return
        
        if self.cur[0] != type:
            raise SyntaxError('Expecting: ' + type + ', But get ' + self.cur[0])
        self.next()
    
    def match_constant(self):
        if self.cur[0] == 'END':
            if self.bracket_stack:
                raise SyntaxError('Bracket no matched!')
            return
        
        if self.cur[0] not in ['constant_int', 'constant_float', 'constant_char', 'constant_string']:
            raise SyntaxError('Expecting: constant, But get ' + self.cur[0])
        self.next()

    def match_delimiter(self):
        if self.cur[0] == 'END':
            if self.bracket_stack:
                raise SyntaxError('Bracket no matched!')
            return
        
        if not self.is_delimiter():
            raise SyntaxError('Expecting: identifiers, But get ' + self.cur[0])
        if self.cur_val in ['(', '{']:
            self.bracket_stack.append(self.cur_val)
        elif self.cur_val in [')', '}']:
            if not self.bracket_stack or \
            (self.cur_val == ')' and self.bracket_stack[-1] != '(') or \
            (self.cur_val == '}' and self.bracket_stack[-1] != '{'):
                raise SyntaxError('Bracket no matched!')
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
        if self.cur[0] == 'keywords' and self.cur_val() in ['int', 'float', 'char', 'void']:
            type_name = self.cur_val()
            self.match_word('keywords')
            return type_name
        else:
            raise SyntaxError('Expecting Keywords!')

    def compound_statement(self):
        self.match_delimiter()
        self.declaration_list()
        self.statement_list()
        self.match_delimiter()

    def declaration_list(self):
        while self.cur[0] == 'keywords':
            self.declaration()

    def declaration(self):
        var_type = self.type()
        identifier = self.cur[1]
        self.match_word('identifiers')
        self.match_delimiter()
        self.compiler.symbol_table.add(identifier, {'type':var_type, 'scope':'local'})

    def statement_list(self):
        while self.cur and self.cur[0] in ['identifiers', 'key_words', 'punctuation']:
            if self.cur_val() == '}':
                return
            self.statement()

    def statement(self):
        if self.cur[0] == 'identifiers':
            self.expr_statement()
        elif self.cur[1] in ['if', 'while']:
            self.control_statement()
        elif self.cur_val() == '{':
            self.compound_statement()
        else:
            self.match_delimiter()

    def expr_statement(self):
        self.expr()
        print(self.cur[0])
        if not self.is_delimiter() or self.cur_val() != ';':
            raise SyntaxError('Missing ";"!')
        self.match_delimiter()

    def control_statement(self):
        if self.cur_val() == 'if':
            self.if_statement()
        elif self.cur_val() == 'while':
            self.while_statement()
        else:
            raise SyntaxError('Unknown control statement!')

    def expr(self):
        return self.assignment_expr()

    def new_label(self):
        self.label_counter += 1
        return f'{self.label_counter}'

    def get_label(self):
        return  f'{self.label_counter}'

    def assignment_expr(self):
        if self.cur[0] == 'identifiers':
            identifier = self.cur_val()
            if not self.compiler.symbol_table.lookup(identifier):
                # print(self.compiler.symbol_table.table)
                raise SyntaxError('Unknown identifier: ' + identifier)
            self.match_word('identifiers')

            if self.cur_val() in ['++', '--']:
                operator = self.cur[1]
                self.match_word('punctuation')
                quad = (self.new_label(), operator, identifier, None, identifier)
                self.compiler.quadruples.append(quad)
                return quad
            else:
                self.match('punctuation')
                if self.cur[0] not in ['identifiers', 'constants_int', 'constants_float', 'constants_char', 'constants_string']:
                    raise SyntaxError('Missing the expression!')
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
        left = self.multiplicative_expression()
        while self.cur[0] == 'punctuation' and self.cur_val() in ['+', '-', '++', '--']:
            operator = self.cur_val()
            self.match_word('punctuation')
            if operator in ['++', '--']:
                right = '1'
            else:
                if self.cur[0] not in ['identifiers', 'constant_int', 'constant_float']:
                    raise SyntaxError('Missing the number after add or sub!')
                right = self.multiplicative_expression()
            temp_var = self.new_temp()
            quad = (self.new_label(), operator, left, right, temp_var)
            self.compiler.quadruples.append(quad)
            left = temp_var
        return left

    def multiplicative_expression(self):
        left = self.factor()
        while self.cur[0] == 'punctuation' and self.cur_val() in ['*', '/']:
            operator = self.cur[1]
            self.match_word('punctuation')
            right = self.factor()
            temp_var = self.new_temp()
            quad = (self.new_label(), operator, left, right, temp_var)
            self.compiler.quadruples.append(quad)
            left = temp_var
        return left

    def while_statement(self):
        self.match_word('keywords')
        self.match_delimiter()
        condition = self.logical_expr()
        self.match_delimiter()
        begin_label = self.get_label()
        start_label = self.new_label()
        self.compiler.quadruples.append((start_label, 'jfalse', condition, None, None))
        jump_location = len(self.compiler.quadruples) - 1
        self.match_delimiter()
        self.statement_list()
        self.match_delimiter()
        self.compiler.quadruples.append((self.new_label(), 'jump', None, None, begin_label))
        end_label = self.new_label()
        self.compiler.quadruples.append((end_label, None, None, None, end_label))
        self.compiler.quadruples[jump_location] = (start_label, 'jfalse', condition, None, end_label)

    def if_statement(self):
        self.match_word('keywords')
        self.match_delimiter()
        condition = self.logical_expr()
        self.match_delimiter()
        start_label = self.new_label()
        self.compiler.quadruples.append((start_label, 'jfalse', condition, None, None))
        jump_location = len(self.quadruples) - 1
        self.match_delimiter()
        self.statement_list()
        self.match_delimiter()
        end_label = self.new_label()
        self.compiler.quadruples.append((end_label, 'jump', None, None, end_label))
        jump_location2 = len(self.quadruples) - 1
        self.compiler.quadruples[jump_location] = (start_label, 'jfalse', condition, None, end_label)
        
        while self.cur and self.cur_val() in ['else']:
            self.match_word('keywords')
            
            if self.cur and self.cur[1] == 'if':
                self.if_statement()
            else:
                self.match_delimiter()
                self.statement_list()
                self.match_delimiter()
        
        self.compiler.quadruples[jump_location2] = (end_label, 'jump', None, None, self.new_label())
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
                raise SyntaxError(identifier + ' is not defined!')
            self.match_word('identifiers')
            return identifier
        elif self.cur[0] in ['constant_int', 'constant_float', 'constant_char', 'constant_string']:
            constant_value = self.cur_val()
            self.match_constant()
            return constant_value

    def new_temp(self):
        if not hasattr(self,'temp_count'):
            self.temp_count = 0
        temp_name = f't{self.temp_count}'
        self.temp_count += 1
        return temp_name

# if __name__ == '__main__':
#     tokens = [
#         ('RESERVE_WORD','int'),
#         ('IDENTIFIER','main'),
#         ('DELIMITER','('),
#         ('DELIMITER',')'),
#         ('DELIMITER','{'),
#         ('RESERVE_WORD','int'),
#         ('IDENTIFIER','number'),
#         ('DELIMITER',';'),
#         ('RESERVE_WORD','int'),
#         ('IDENTIFIER','a'),
#         ('DELIMITER',';'),
#         ('IDENTIFIER','number'),
#         ('OPERATOR','='),
#         ('CONSTANT','10'),
#         ('DELIMITER',';'),
#         ('RESERVE_WORD','if'),
#         ('DELIMITER','('),
#         ('IDENTIFIER','number'),
#         ('OPERATOR','>'),
#         ('CONSTANT','0'),
#         ('DELIMITER',')'),
#         ('DELIMITER','{'),
#         ('IDENTIFIER','a'),
#         ('OPERATOR','='),
#         ('IDENTIFIER','number'),
#         ('DELIMITER',';'),
#         ('DELIMITER','}'),
#         ('RESERVE_WORD','else'),
#         ('DELIMITER','{'),
#         ('IDENTIFIER','a'),
#         ('OPERATOR','='),
#         ('CONSTANT','2'),
#         ('DELIMITER',';'),
#         ('DELIMITER','}'),
#         ('DELIMITER','}')
#     ]



#     # 创建解析器实例
#     parser = Parser(tokens)

#     # 开始解析

#     parser.program()
#     print(parser.symbol_table.table)
#     # 如果没有抛出SyntaxError异常，说明解析成功
#     print('解析成功！')
#     print(parser.quadruples)