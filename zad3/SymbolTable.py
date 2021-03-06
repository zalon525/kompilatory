#!/usr/bin/python


class Symbol:
    pass


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class FunctionSymbol(Symbol):
    def __init__(self, name, type, table):
        self.name = name
        self.type = type
        self.table = table
        self.param_types = []

    def setParamTypesFromTable(self):
        self.param_types = [symbol.type for symbol in self.table.entries.values()]


class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.entries = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.entries[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        try:
            return self.entries[name]
        except KeyError:
            return None

    def getParentScope(self):
        return self.parent

    def getFromAnyEnclosingScope(self, name):
        if self.get(name) is None:
            if self.getParentScope() is not None:
                return self.parent.getFromAnyEnclosingScope(name)
            else:
                return None
        else:
            return self.get(name)
