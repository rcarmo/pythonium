from ast import NodeVisitor
from io import StringIO


class YieldSearch(NodeVisitor):

    def visit_Yield(self, node):
        self.has_yield = True

    def visit_FunctionDef(self, node):
        pass  # do not visit nest function definition to determine
              # if a function has a yield or not...



class Writer:

    def __init__(self):
        self.level = 0
        self.output = StringIO()

    def push(self):
        self.level += 1

    def pull(self):
        self.level -= 1

    def write(self, code):
        self.output.write(' ' * 4 * self.level + code + '\n')

    def value(self):
        return self.output.getvalue()
