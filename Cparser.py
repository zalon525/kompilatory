#!/usr/bin/python

from scanner import Scanner
import AST



class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    
    
    def p_program(self, p):
        """program : segments"""
        p[0] = AST.Program(p[1])

    def p_segments(self, p):
        """segments : segments segment
                    | segment"""

        segments = None
        segment = None

        if len(p) > 2:
            segments = p[1]
            segment = p[2]
        else:
            segment = p[1]

        p[0] = AST.Segments(segments, segment)

    # def p_declarations(self, p):
    #     """declarations : declarations declaration
    #                     | """
    #     declarations = None
    #     declaration = None
    #
    #     if len(p) == 3:
    #         declarations = p[1]
    #         declaration = p[2]
    #
    #     p[0] = AST.Declarations(p[1], p[2])

    def p_segment(self, p):
        """segment : fundef
                   | instruction
                   | declaration"""
        p[0] = p[1]
    
    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        type = None
        inits = None
        error = None

        if len(p) > 3:
            type = p[1]
            inits = p[2]
        else:
            error = p[1]

        p[0] = AST.Declaration(type, inits, error)


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        inits = None
        init = None

        if(len(p) > 2):
            inits = p[1]
            init = p[3]
        else:
            init = p[1]

        p[0] = AST.Inits(inits, init)


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = AST.Init(p[1], p[3])
 

    # def p_instructions_opt(self, p):
    #     """instructions_opt : instructions
    #                         | """

    
    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        instructions = None
        instruction = None

        if len(p) > 2:
            instructions = p[1]
            instruction = p[2]
        else:
            instruction = p[1]

        p[0] = AST.Instructions(instructions, instruction)
    
    
    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]
    
    
    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        p[0] = AST.PrintInstruction(p[2])

    
    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstruction(p[1], p[3])
    
    
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.Assignment(p[1], p[3])
    
    
    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        condition = p[3]
        instruction = p[5]
        else_instruction = None

        if(len(p) > 7):
            else_instruction = p[7]

        p[0] = AST.ChoiceInstruction(condition, instruction, else_instruction)
    
    
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstruction(p[3], p[5])


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstruction(p[2], p[4])
    
    
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstruction(p[2])

    
    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstruction()

    
    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstruction()
    
    
    def p_compound_instr(self, p):
        """compound_instr : '{' segments '}' """

        p[0] = AST.CompoundInstruction(p[2])

    
    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        p[0] = p[1]
    
    
    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """

        if len(p) == 2:
            p[0] = AST.Const(p[1])
        elif p[1] == '(' and p[3] == ')':
            p[0] = AST.ParenExpression(p[2])
        elif p[2] == '(' and p[1] != '(':
            p[0] = AST.FunctionExpression(p[1], p[3])
        else:
            p[0] = AST.BinExpr(p[2], p[1], p[3])
    
    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        expr_list = None

        if len(p) > 1:
           expr_list = p[1]

        p[0] = AST.ExpressionList(expr_list, None)

    
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        expr_list = None
        expression = None

        if len(p) > 2:
            expr_list = p[1]
            expression = p[3]
        else:
            expression = p[1]

        p[0] = AST.ExpressionList(expr_list, expression)
    

    # def p_fundefs_opt(self, p):
    #     """fundefs_opt : fundefs
    #                    | """
    #
    # def p_fundefs(self, p):
    #     """fundefs : fundefs fundef
    #                | fundef """
    #     # gramatyka?
    #

          
    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.Fundef(p[1], p[2], p[4], p[6])
    
    
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        args_list = None

        if len(p) > 1:
            args_list = p[1]

        p[0] = AST.ArgumentsList(args_list, None)
    
    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """

        args_list = None
        arg = None

        if len(p) > 2:
            args_list = p[1]
            arg = p[3]
        else:
            arg = p[1]

        p[0] = AST.ArgumentsList(args_list, arg)
    
    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Argument(p[1], p[2])


    