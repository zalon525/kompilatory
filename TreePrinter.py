
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def print_indent(string, indent):
    print "| " * indent + string


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print_indent(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)
        # ...

    @addToClass(AST.Const)
    def printTree(self, indent):
        print_indent(str(self.value), indent)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.segments.printTree(indent)

    @addToClass(AST.Segments)
    def printTree(self, indent=0):
        for segment in self.segments:
            segment.printTree(indent)

    # @addToClass(AST.Declarations)
    # def printTree(self, indent=0):
    #     for declaration in self.declarations:
    #         declaration.printTree(indent)

    @addToClass(AST.Declaration)
    def printTree(self, indent=0):
        if not self.error:
            print_indent("DECL", indent)
            self.inits.printTree(indent + 1)

    @addToClass(AST.Inits)
    def printTree(self, indent=0):
        for init in self.inits:
            init.printTree(indent)

    @addToClass(AST.Init)
    def printTree(self, indent=0):
        print_indent("=", indent)
        print_indent(self.id, indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)


    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        print_indent("PRINT", indent)
        self.expr_list.printTree(indent)

    @addToClass(AST.LabeledInstruction)
    def printTree(self, indent=0):
        print_indent(self.id + ":", indent)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent):
        print_indent("=", indent)
        print_indent(self.id, indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, indent=0):
        print_indent("IF", indent)
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

        if self.else_instruction:
            print_indent("ELSE", indent)
            self.else_instruction.printTree(indent + 1)

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent):
        print_indent("WHILE", indent)
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.RepeatInstruction)
    def printTree(self, indent):
        print_indent("REPEAT", indent)
        self.instructions.print_tree(indent + 1)
        print_indent("UNTIL", indent)
        self.condition.print_tree(indent + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent):
        print_indent("RETURN", indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent):
        print_indent("BREAK", indent)

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent):
        print_indent("CONTINUE", indent)

    @addToClass(AST.CompoundInstruction)
    def printTree(self, indent):
        self.segments.printTree(indent)

    @addToClass(AST.ParenExpression)
    def printTree(self, indent):
        self.expression.printTree(indent)

    @addToClass(AST.FunctionExpression)
    def printTree(self, indent):
        print_indent("FUNCALL", indent)
        print_indent(self.id, indent + 1)
        self.expr_list.printTree(indent + 1)

    @addToClass(AST.ExpressionList)
    def printTree(self, indent):
        for expression in self.expr_list:
            expression.printTree(indent + 1)

    @addToClass(AST.Fundef)
    def printTree(self, indent):
        print_indent("FUNDEF", indent)
        print_indent(self.id, indent + 1)
        print_indent("RET " + self.type, indent + 1)
        self.args_list.printTree(indent + 1)
        self.compound_instr.printTree(indent + 1)

    @addToClass(AST.ArgumentsList)
    def printTree(self, indent):
        for arg in self.args_list:
            arg.printTree(indent)

    @addToClass(AST.Argument)
    def printTree(self, indent):
        print_indent("ARG " + self.id, indent)

    # @addToClass ...
    # ...