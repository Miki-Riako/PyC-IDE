class SymbolTable:
    def __init__(self):
        self.table = {}

    def add(self, identifier, info):
        self.table[identifier] = info

    def lookup(self, identifier):
        return self.table.get(identifier, None)
