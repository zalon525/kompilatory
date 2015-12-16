#!/usr/bin/python
from collections import defaultdict

import AST
from SymbolTable import SymbolTable, VariableSymbol, FunctionSymbol

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
        self.symbolTable = SymbolTable(None, 'root')
        self.declType = ''
        self.curFunc = None

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
        definition = self.symbolTable.getFromAnyEnclosingScope(node)

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
            if self.symbolTable.get(node.name) is not None:
                print "Symbol {} in line {} is already defined in this scope".format(node.name, node.line)
            else:
                self.symbolTable.put(node.name, VariableSymbol(node.name, self.declType))
        else:
            print "Type mismatch in assignment of {} to {}. Line {}".format(initType, self.declType, node.line)

    def visit_Assignment(self, node):
        definition = self.symbolTable.getFromAnyEnclosingScope(node.id)
        type = self.visit(node.expr)

        if definition is None:
            print "Assignment to undefined symbol {}. Line {}".format(node.id, node.line)
        elif type != definition.type and (definition.type != "float" and definition != "int"):
            print "Type mismatch in assignment of {} to {}. Line {}.".format(type, definition.type, node.line)

    def visit_ParenExpression(self, node):
        self.visit(node.expression)

    def visit_Fundef(self, node):
        if self.symbolTable.get(node.id) is not None:
            print "Function {} in line {} is already defined in this scope".format(node.id, node.line)
        else:
            func = FunctionSymbol(node.id, node.type, SymbolTable(self.symbolTable, node.id))
            self.symbolTable.put(node.id, func)
            self.curFunc = func
            self.symbolTable = func.table
            if node.args_list is not None:
                self.visit(node.args_list)
            self.visit(node.compound_instr)
            self.symbolTable = self.symbolTable.getParentScope()
            self.curFunc = None

    def visit_CompoundInstruction(self, node):
        innerScope = SymbolTable(self.symbolTable, "innerScope")
        self.symbolTable = innerScope
        self.visit(node.segments)
        self.symbolTable = self.symbolTable.getParentScope()

    def visit_PrintInstruction(self, node):
        self.visit(node.expr_list)

    def visit_LabeledInstruction(self, node):
        self.visit(node.instruction)

    def visit_ChoiceInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)
        self.visit(node.else_instruction)

    def visit_WhileInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)

    def visit_RepeatInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.instructions)

    def visit_ReturnInstruction(self, node):
        if self.curFunc is None:
            print "Return statement outside of a function. Line {}".format(node.line)
        else:
            type = self.visit(node.expression)
            if type != self.curFunc.type and (self.curFunc.type != "float" or type != "int"):
                print "Invalid return type of {} in line {}. Expected {}".format(type, node.line, self.curFunc.type)

    def visit_FunctionExpression(self, node):
        funDef = self.symbolTable.getFromAnyEnclosingScope(node.id)
        if funDef is None or not isinstance(funDef, FunctionSymbol):
            print "Function {} not defined. Line: {}".format(node.id, node.line)
        else:
            if node.expr_list is None and funDef.params != []:
                print "Invalid number of arguments in line {}. Expected {}". \
                    format(node.line, len(funDef.params))
            else:
                types = [self.visit(x) for x in node.expr_list.children]
                expectedTypes = funDef.params
                for actual, expected in zip(types, expectedTypes):
                    if actual != expected and not (actual == "int" and expected == "float"):
                        print "Mismatching argument types in line {}. Expected {}, got {}". \
                            format(node.line, expected, actual)
            return funDef.type
