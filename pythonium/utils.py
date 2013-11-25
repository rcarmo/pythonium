from ast import NodeVisitor


class YieldSearch(NodeVisitor):

    def visit_Yield(self, node):
        self.has_yield = True
