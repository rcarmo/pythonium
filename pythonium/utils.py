from ast import NodeVisitor


class YieldSearch(NodeVisitor):

    def visit_Yield(self, node):
        self.has_yield = True

    def visit_FunctionDef(self, node):
        pass  # do not visit nest function definition to determine
              # if a function has a yield or not...
