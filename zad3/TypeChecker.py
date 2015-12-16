#!/usr/bin/python
from collections import defaultdict

import AST
from SymbolTable import SymbolTable, VariableSymbol

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, 'root')
        self.declType = ''

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        oper = node.op

        if ttype[oper][type1][type2] is None:
            print "Invalid binary expresion {}. Line: {}".format(oper, node.line)
        return ttype[oper][type1][type2]

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        definition = self.table.getFromAnyEnclosingScope(node)

        if definition is None:
            "Undefined symbol {}. Line: {}".format(node.name, node.line)
        else:
            return definition.type

    def visit_Program(self, node):
        self.visit(node.segments)

    def visit_Declaration(self, node):
        self.declType = node.type
        self.visit(node.inits)
        self.declType = ''

    def visit_Init(self, node):
        initType = self.visit(node.expr)
        if initType == self.declType or (initType == "int" and self.declType == "float") or (
                        initType == "float" and self.declType == "int"):
            if self.table.get(node.name) is not None:
                print "Symbol {} in line {} is already defined earlier".format(node.name, node.line)
            else:
                self.table.put(node.name, VariableSymbol(node.name, self.declType))
        else:
            print "Type mismatch in assignment of {} to {}. Line {}".format(initType, self.declType, node.line)
