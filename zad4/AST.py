

class Node:

    def accept(self, visitor):
        return visitor.visit(self)
