class Node(object):
    def __str__(self):
        return self.printTree()


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class Const(Node):
    def __init__(self, value):
        self.value = value
        # ...


class Integer(Const):
    pass
    # ...


class Float(Const):
    pass
    # ...


class String(Const):
    pass
    # ...


class Variable(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line


class Program(Node):
    def __init__(self, segments):
        self.segments = segments


class Segments(Node):
    def __init__(self, segments, segment):
        self.segments = []
        if segments:
            self.segments.extend(segments.segments)
        if segment:
            self.segments.append(segment)

        self.children = self.segments


class Segment(Node):
    pass


class Declarations(Node):
    def __init__(self, declarations, declaration):
        self.declarations = []

        if declarations:
            self.declarations.extend(declarations.declarations)

        if declaration:
            self.declarations.append(declaration)

        self.children = self.declarations


class Declaration(Node):
    def __init__(self, type, inits, error):
        self.type = type
        self.inits = inits
        self.error = error


class Inits(Node):
    def __init__(self, inits, init):
        self.inits = []

        if inits:
            self.inits.extend(inits.inits)

        if init:
            self.inits.append(init)

        self.children = self.inits


class Init(Node):
    def __init__(self, name, expression, line):
        self.name = name
        self.expression = expression
        self.line = line


class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = []

        if instructions:
            self.instructions.extend(instructions.instructions)

        if instruction:
            self.instructions.append(instruction)

        self.children = self.instructions


class Instruction(Node):
    pass


class PrintInstruction(Instruction):
    def __init__(self, expr_list):
        self.expr_list = expr_list


class LabeledInstruction(Instruction):
    def __init__(self, id, instruction):
        self.instruction = instruction
        self.id = id


class Assignment(Node):
    def __init__(self, id, expression):
        self.expression = expression
        self.id = id


class ChoiceInstruction(Node):  # spr
    def __init__(self, condition, instruction, else_instruction):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction


class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.condition = condition
        self.instructions = instructions


class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class CompoundInstruction(Node):
    def __init__(self, segments):
        self.segments = segments


class Condition(Node):
    pass


class Expression(Node):
    pass


class ExpressionList(Node):
    def __init__(self, expr_list, expression):
        self.expr_list = []

        if expr_list:
            self.expr_list.extend(expr_list.expr_list)

        if expression:
            self.expr_list.append(expression)


class ParenExpression(Node):
    def __init__(self, expression):
        self.expression = expression


class FunctionExpression(Node):
    def __init__(self, id, expr_list):
        self.id = id
        self.expr_list = expr_list


class Fundef(Node):
    def __init__(self, type, id, args_list, compound_instr):
        self.type = type
        self.id = id
        self.args_list = args_list
        self.compound_instr = compound_instr


class ArgumentsList(Node):
    def __init__(self, args_list, arg):
        self.args_list = []

        if args_list:
            self.args_list.extend(args_list.args_list)

        if arg:
            self.args_list.append(arg)

        self.children = self.args_list


class Argument(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id

# ...
