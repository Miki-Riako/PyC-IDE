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
    assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': '2'}"

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


def test_c4():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int a, b, c;
    a = 1;
    b = 1;
    while (a > 0) {
        c = a + b;
        a--;
    }
    if (c > 0) {
        c = -2;
    }
}
    '''
    compiler.compile()

    assert compiler.error == ''


def test_c5():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int a, b, c;
    a = 1;
    b = 1
    while (a > 0) {
        c = a + b;
        a--;
    }
    if (c > 0) {
        c = -2;
    }
}
    '''
    try:
        compiler.compile()
        assert False
    except Exception:
        assert compiler.error == 'Missing ";"!'

def test_c6():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int b, c;
    a = 1;
    b = 1
    while (a > 0) {
        c = a + b;
        a--;
    }
    if (c > 0) {
        c = -2;
    }
}
    '''
    try:
        compiler.compile()
        assert False
    except Exception:
        assert compiler.error == 'Unknown identifier: a'

def test_c7():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int a, b, c;
    a = 1;
    b = 1;
    while (a > 0) {
        c = a + b;
        a--;
    }
    if (c > 0) {
        c = -2;
    }

    '''
    try:
        compiler.compile()
        assert False
    except Exception:
        assert compiler.error == "Bracket not matched!"

def test_c8():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int a, b, c;
    a = 1;
    b = 1;
    while (a > 0) {
        c = a + b;
        a--;
    }
    if (c > 0) {
        c = -2;
    }
}
}
    '''
    try:
        compiler.compile()
        assert False
    except Exception:
        assert compiler.error == "Expecting keyword, But got }"

def test_c9():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int num;
    char a;
    num = 2;
    if (num > 0) {
        a = 'n';
    } else if (num == 0) {
        a = 'e';
    } else {
        a = 'u';
    }
}
    '''
    compiler.compile()

    assert compiler.error == ''
    assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('keywords', 14), ('identifiers', 2), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_char', 0), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 4), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_char', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_char', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    assert str(compiler.quadruples) == "[('1', '=', '2', None, 'num'), ('2', '>', 'num', '0', 't0'), ('3', 'jf', 't0', None, '6'), ('4', '=', 'n', None, 'a'), ('5', 'jmp', None, None, '14'), ('6', None, None, None, None), ('7', '==', 'num', '0', 't1'), ('8', 'jf', 't1', None, '11'), ('9', '=', 'e', None, 'a'), ('10', 'jmp', None, None, '13'), ('11', None, None, None, None), ('12', '=', 'u', None, 'a'), ('13', None, None, None, None), ('14', None, None, None, None)]"
    assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': 'n'}"

def test_c10():
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
    return 0;
}
    '''
    compiler.compile()

    assert compiler.error == ''
    # assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('keywords', 0), ('identifiers', 2), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('identifiers', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    # assert str(compiler.quadruples) == "[('1', '=', '2', None, 'num'), ('2', '>', 'num', '0', 't0'), ('3', 'jf', 't0', None, '6'), ('4', '=', 'num', None, 'a'), ('5', 'jmp', None, None, '8'), ('6', None, None, None, None), ('7', '=', '1', None, 'a'), ('8', None, None, None, None)]"
    # assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': '2'}"

def test_c11():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int num;
    int a;
    num = 2;
    do {
        a = num;
        a--;
        num = a;
    } while (num > 0);
}
    '''
    compiler.compile()

    assert compiler.error == ''
    # assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('keywords', 0), ('identifiers', 2), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('identifiers', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    # assert str(compiler.quadruples) == "[('1', '=', '2', None, 'num'), ('2', '>', 'num', '0', 't0'), ('3', 'jf', 't0', None, '6'), ('4', '=', 'num', None, 'a'), ('5', 'jmp', None, None, '8'), ('6', None, None, None, None), ('7', '=', '1', None, 'a'), ('8', None, None, None, None)]"
    # assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': '2'}"


def test_c12():
    compiler = Compiler()
    compiler.code = '''
int make(int b, int c) {
    return 2 + 3;
}

int main() {
    int num;
    int a, y;
    num = 2;
    if (num < 0) {
        a = num;
    } else {
        a = 1;
        y = make(a, num);
    }
}
    '''
    compiler.compile()

    assert compiler.error == ''
    # assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('keywords', 0), ('identifiers', 2), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('identifiers', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    # assert str(compiler.quadruples) == "[('1', '=', '2', None, 'num'), ('2', '>', 'num', '0', 't0'), ('3', 'jf', 't0', None, '6'), ('4', '=', 'num', None, 'a'), ('5', 'jmp', None, None, '8'), ('6', None, None, None, None), ('7', '=', '1', None, 'a'), ('8', None, None, None, None)]"
    # assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': '2'}"

def test_c13():
    compiler = Compiler()
    compiler.code = '''
int main() {
    int num;
    int a, i;
    num = 2;
    for (i = 0; i < 5; i++) {
        num = num * 2;
    }
}
    '''
    compiler.compile()

    assert compiler.error == ''
    # assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('keywords', 0), ('identifiers', 2), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('identifiers', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
    # assert str(compiler.quadruples) == "[('1', '=', '2', None, 'num'), ('2', '>', 'num', '0', 't0'), ('3', 'jf', 't0', None, '6'), ('4', '=', 'num', None, 'a'), ('5', 'jmp', None, None, '8'), ('6', None, None, None, None), ('7', '=', '1', None, 'a'), ('8', None, None, None, None)]"
    # assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': '2'}"


# def test_c14():
#     compiler = Compiler()
#     compiler.code = '''
# struct A {int n1; int n2;};
# int main() {
#     struct A a;
#     a.n1 = 1;
#     a.n2 = 2;
#     return 0;
# }
#     '''
#     compiler.compile()

#     assert compiler.error == ''
#     # assert str(compiler.tokens) == "[('keywords', 0), ('identifiers', 0), ('punctuation', 2), ('punctuation', 3), ('punctuation', 14), ('keywords', 0), ('identifiers', 1), ('punctuation', 12), ('keywords', 0), ('identifiers', 2), ('punctuation', 12), ('identifiers', 1), ('punctuation', 10), ('constants_int', 0), ('punctuation', 12), ('keywords', 11), ('punctuation', 2), ('identifiers', 1), ('punctuation', 9), ('constants_int', 1), ('punctuation', 3), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('identifiers', 1), ('punctuation', 12), ('punctuation', 15), ('keywords', 13), ('punctuation', 14), ('identifiers', 2), ('punctuation', 10), ('constants_int', 2), ('punctuation', 12), ('punctuation', 15), ('punctuation', 15), ('END', -1)]"
#     # assert str(compiler.quadruples) == "[('1', '=', '2', None, 'num'), ('2', '>', 'num', '0', 't0'), ('3', 'jf', 't0', None, '6'), ('4', '=', 'num', None, 'a'), ('5', 'jmp', None, None, '8'), ('6', None, None, None, None), ('7', '=', '1', None, 'a'), ('8', None, None, None, None)]"
#     # assert str(compiler.variables) == "{'num': '2', 't0': True, 'a': '2'}"

