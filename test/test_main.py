import os, sys
import pytest
from _compiler import Compiler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_c1():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int num;
    int a;
    num = 2;
    if (num > 0) {
        a = num;
    } else {
        a = 1;
    }
}
    '''
    compiler.compile()

    assert compiler.error == ''
    assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('keywords', 0), ('identifiers', 2), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('identifiers', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    assert str(compiler.quadruples) == "[('1', '=', '2', None, 'num'), ('2', '>', 'num', '0', 't0'), ('3', 'jf', 't0', None, '6'), ('4', '=', 'num', None, 'a'), ('5', 'jmp', None, None, '8'), ('6', None, None, None, None), ('7', '=', '1', None, 'a'), ('8', None, None, None, None)]"
    assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': '1'}"

def test_c2():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int a ;
    a=5;
    if (a > 3) {
        a = a + 2;
    }
}
    '''
    compiler.compile()

    assert compiler.error == ''
    assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 1), ('punctuation', 10), ('identifiers', 1), ('punctuation', 7), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    assert str(compiler.quadruples) == "[('1', '=', '5', None, 'a'), ('2', '>', 'a', '3', 't0'), ('3', 'jf', 't0', None, '7'), ('4', '+', 'a', '2', 't1'), ('5', '=', 't1', None, 'a'), ('6', 'jmp', None, None, '8'), ('7', None, None, None, None), ('8', None, None, None, None)]"
    assert str(compiler.variables) == "{'a': 7, 't0': True, 't1': 7}"


def test_c3():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int num;
    num = 1;
    num = 0;
    int a;
    if (num > 0) {
        a = num;
    } else {
        a = 2;
    }
}
    '''
    compiler.compile()

    assert compiler.error == ''
    assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 1), ('punctuation', 12), ('keywords', 0), ('identifiers', 2), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('identifiers', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    assert str(compiler.quadruples) == "[('1', '=', '1', None, 'num'), ('2', '=', '0', None, 'num'), ('3', '>', 'num', '0', 't0'), ('4', 'jf', 't0', None, '7'), ('5', '=', 'num', None, 'a'), ('6', 'jmp', None, None, '9'), ('7', None, None, None, None), ('8', '=', '2', None, 'a'), ('9', None, None, None, None)]"
    assert str(compiler.variables) == "{'num': '0', 't0': False, 'a': '2'}"
