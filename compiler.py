from scanner import Scanner, Parser, get_token

class Compiler:
    def __init__(self):
        self.scanner = Scanner()
        self.parser = Parser()

    def compile(self, code):
        self.scanner.scan(code)
        if self.scanner.error:
            print("Lexical Error")
            return False
        tokens = get_token(self.scanner)
        if self.parser.parse(tokens):
            print("Parsing Successful")
            return True
        else:
            print("Syntax Error")
            return False

if __name__ == "__main__":
    code = input("Enter code: ")
    compiler = Compiler()
    result = compiler.compile(code)
    print(result)