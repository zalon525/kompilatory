class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.dict = {}

    def has_key(self, name):  # variable name
        return self.dict.has_key(name)

    def get(self, name):  # gets from memory current value of variable <name>
        return self.dict.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.dict[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = []

        if memory is not None:
            self.push(memory)

    def get(self, name):  # gets from memory stack current value of variable <name>
        return self.stack[-1].get(name)

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        self.stack[-1].put(name, value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        return self.stack.pop()