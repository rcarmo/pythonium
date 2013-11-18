#!/usr/bin/env python3
"""pythonium_core

Usage: pythonium_core [-h][-d][-r] FILE [FILE ...] [-o FILE]

Options:
  -h --help        show this
  -v --version     show version
  -o --output FILE specify output file [default: stdout]
  -d --deep        generate file dependencies. If --output is not provided, it will generate for each source file a coresponding .js file.
  -r --requirejs   generate requirejs compatible module
"""
import os
import sys

from ast import Str
from ast import Name
from ast import List
from ast import Tuple
from ast import parse
from ast import Assign
from ast import Global
from ast import FunctionDef
from ast import NodeVisitor


__version__ = '0.2.5'


class PythoniumCore(NodeVisitor):

    def __init__(self):
        super().__init__()
        self.dependencies = []
        self.in_classdef = None
        self._function_stack = []
        self.__all__ = None

    def visit(self, node):
        if os.environ.get('DEBUG', False):
            print(">>>", node.__class__.__name__, node._fields)
        return super().visit(node)

    def visit_Pass(self, node):
        return ''

    def visit_Try(self, node):
        out = 'try {\n'
        out += '\n'.join(map(self.visit, node.body))
        out += '\n}\n'
        out += 'catch(__exception__) {\n'
        out += '\n'.join(map(self.visit, node.handlers))
        out += '\n}\n'
        return out

    def visit_Raise(self, node):
        return 'throw {};'.format(self.visit(node.exc))

    def visit_ExceptHandler(self, node):
        return '\n'.join(map(self.visit, node.body)) + '\n'

    def visit_Yield(self, node):
        return 'yield {};'.format(self.visit(node.value))

    def visit_In(self, node):
        return ' in '

    def visit_Module(self, node):
        return '\n'.join(map(self.visit, node.body))

    def visit_Tuple(self, node):
        return '[{}]'.format(', '.join(map(self.visit, node.elts)))

    def visit_List(self, node):
        return '[{}]'.format(', '.join(map(self.visit, node.elts)))

    def visit_ImportFrom(self, node):
        if len(node.names) > 1:
            raise NotImplemented
        if len(node.names) == 0:
            raise NotImplemented
        out = ''
        name = node.names[0].name
        asname = node.names[0].asname
        if not asname:
            asname = name
        modules = '/'.join(node.module.split('.'))
        path = modules + '/' + name
        if node.level == 0:
            out = 'var {} = require("{}");'.format(asname, path)
            self.dependencies.append('/' + path)  # relative to project root
        elif node.level == 1:
            out = 'var {} = require.toUrl("./{}");'.format(asname, path)
            self.dependencies.append('./' + path)  # relative to current file
        else:
            path = '../' * node.level + path
            out = 'var {} = require.toUrl("{}");'.format(asname, path)
            self.dependencies.append(path)  # relative to current file
        return out

    def visit_Global(self, node):
        # handled in visit_FunctionDef
        return ''

    def visit_FunctionDef(self, node):
        # 'name', 'args', 'body', 'decorator_list', 'returns'
        self._function_stack.append(node.name)
        args, kwargs, varargs, varkwargs = self.visit(node.args)

        if self.in_classdef and len(self._function_stack) == 1:
            __args = ', '.join(args[1:])
            buffer = '{}: function({}) {{\n'.format(node.name, __args)
        else:
            __args = ', '.join(args)
            buffer = 'var {} = function({}) {{\n'.format(node.name, __args)
        if not varkwargs:
            varkwargs = '__kwargs'
        
        # unpack arguments
        buffer += 'var __args = Array.prototype.slice.call(arguments);\n'
        buffer += 'var {} = __args[__args.length - 1];\n'.format(varkwargs)
        for keyword in kwargs.keys():
            buffer += '{} = {} || {}.{} || {};\n'.format(keyword, keyword, varkwargs, keyword, kwargs[keyword])
            buffer += 'delete {}.{};\n'.format(varkwargs, keyword)
        if varargs:
            buffer += 'var {} = __args.splice({});\n'.format(varargs, len(args))
            buffer += '{}.pop();\n'.format(varargs)
        # check for variable creation use var if not global
        def retrieve_vars(body):
            local_vars = set()
            global_vars = set()
            for n in body:
                if isinstance(n, Assign) and isinstance(n.targets[0], Name):
                    local_vars.add(n.targets[0].id)
                elif isinstance(n, Global):
                    global_vars.update(n.names)
                elif hasattr(n, 'body') and not isinstance(n, FunctionDef):
                    # do a recursive search inside new block except function def
                    l, g = retrieve_vars(n.body)
                    local_vars.update(l)
                    global_vars.update(g)
                    if hasattr(n, 'orelse'):
                        l, g = retrieve_vars(n.orelse)
                        local_vars.update(l)
                        global_vars.update(g)
            return local_vars, global_vars

        local_vars, global_vars = retrieve_vars(node.body)

        if local_vars - global_vars:
            a = ','.join(local_vars-global_vars)
            buffer += 'var {};\n'.format(a)

        # output function body
        body = '\n'.join(map(self.visit, node.body))
        buffer += body
        if self.in_classdef and len(self._function_stack) == 1:
            buffer += '\n},\n'
        else:
            buffer += '\n};\n'

        self._function_stack.pop()
        return buffer

    def visit_Subscript(self, node):
        return '{}[{}]'.format(self.visit(node.value), self.visit(node.slice.value))

    def visit_arguments(self, node):
        # 'args', 'vararg', 'varargannotation', 'kwonlyargs', 'kwarg', 'kwargannotation', 'defaults', 'kw_defaults'
        args = list(map(lambda x: x.arg, node.args))
        vararg = node.vararg
        kwonlyargs = node.kwonlyargs
        varkwargs = node.kwarg
        defaults = list(map(self.visit, node.defaults))
        kwargs = dict(zip(args[-len(defaults):], defaults))
        return args, kwargs, vararg, varkwargs

    def visit_Name(self, node):
        if node.id == 'None':
            return 'undefined'
        elif node.id == 'self':
            return 'this'
        elif node.id == 'True':
            return 'true'
        elif node.id == 'False':
            return 'false'
        elif node.id == 'null':
            return 'null'
        return node.id.replace('__DOLLAR__', '$')

    def visit_Attribute(self, node):
        name = self.visit(node.value)
        attr = node.attr
        return '{}.{}'.format(name, attr)

    def visit_keyword(self, node):
        if isinstance(node.arg, str):
            return node.arg, self.visit(node.value)
        return self.visit(node.arg), self.visit(node.value)

    def visit_Call(self, node):
        name = self.visit(node.func)
        if name == 'instanceof':
            # this gets used by "with javascript:" blocks
            # to test if an instance is a JavaScript type
            args = list(map(self.visit, node.args))
            if len(args) == 2:
                return '{} instanceof {}'.format(*tuple(args))
            else:
                raise SyntaxError(args)
        elif name == 'JSObject':
            if node.keywords:
                kwargs = map(self.visit, node.keywords)
                f = lambda x: '"{}": {}'.format(x[0], x[1])
                out = ', '.join(map(f, kwargs))
                return '{{}}'.format(out)
            else:
                return 'Object()'
        elif name == 'var':
            args = map(self.visit, node.args)
            out = ', '.join(args)
            return 'var {}'.format(out)
        elif name == 'new':
            args = list(map(self.visit, node.args))
            object = args[0]
            args = ', '.join(args[1:])
            return 'new {}({})'.format(object, args)
        elif name == 'super':
            args = ', '.join(map(self.visit, node.args))
            return 'this.$super({})'.format(args)
        elif name == 'JSArray':
            if node.args:
                args = map(self.visit, node.args)
                out = ', '.join(args)
            else:
                out = ''
            return '[{}]'.format(out)
        elif name == 'JS':
            return node.args[0].s
        elif name == 'print':
            args = [self.visit(e) for e in node.args]
            s = 'console.log({});'.format(', '.join(args))
            return s
        else:
            if node.args:
                args = [self.visit(e) for e in node.args]
                args = ', '.join([e for e in args if e])
            else:
                args = ''
            return '{}({})'.format(name, args)

    def visit_While(self, node):
        body = '\n'.join(map(self.visit, node.body))
        return 'while({}) {{\n{}\n}}'.format(self.visit(node.test), body)

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        return '{} = {} {} {}'.format(target, target, self.visit(node.op), self.visit(node.value))

    def visit_Str(self, node):
        s = node.s.replace('\n', '\\n')
        if '"' in s:
            return "'{}'".format(s)
        return '"{}"'.format(s)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return '({} {} {})'.format(left, op, right)

    def visit_Mult(self, node):
        return '*'

    def visit_Add(self, node):
        return '+'

    def visit_Sub(self, node):
        return '-'

    def visit_USub(self, node):
        return '-'

    def visit_Div(self, node):
        return '/'

    def visit_Mod(self, node):
        return '%'

    def visit_Lt(self, node):
        return '<'

    def visit_Gt(self, node):
        return '>'

    def visit_GtE(self, node):
        return '>='

    def visit_LtE(self, node):
        return '<='

    def visit_LShift(self, node):
        return '<<'

    def visit_RShift(self, node):
        return '>>'

    def visit_BitXor(self, node):
        return '^'

    def visit_BitOr(self, node):
        return '|'

    def visit_BitAnd(self, node):
        return '&'

    def visit_Eq(self, node):
        return '=='

    def visit_NotEq(self, node):
        return '!='

    def visit_Num(self, node):
        return str(node.n)

    def visit_Is(self, node):
        return '==='

    def visit_Not(self, node):
        return '!'

    def visit_IsNot(self, node):
        return '!=='

    def visit_UnaryOp(self, node):
        return self.visit(node.op) + self.visit(node.operand)

    def visit_And(self, node):
        return '&&'

    def visit_Or(self, node):
        return '||'

    def visit_Assign(self, node):
        # XXX: I'm not sure why it is a list since, mutiple targets are inside a tuple
        target = node.targets[0]
        if isinstance(target, Tuple):
            raise NotImplementedError
        else:
            target = self.visit(target)
            value = self.visit(node.value)
            if self.in_classdef and len(self._function_stack) == 0:
                code = '{}: {},'.format(target, value)
            else:
                if target == '__all__':
                    if isinstance(node.value, Name):
                        self.__all__ = value
                    elif isinstance(node.value, Str):
                        self.__all__ = node.value.s
                    elif isinstance(node.value, List):
                        if isinstance(node.value.elts[0], Name):
                            self.__all__ = list(map(self.visit, node.value.elts))
                        else:
                            self.__all__ = list(map(lambda x: x.s, node.value.elts))
                    else:
                        raise NotImplementedError
                    code = ''
                else:
                    code = '{} = {};'.format(target, value)
            return code

    def visit_Expr(self, node):
        s = self.visit(node.value)
        if not s.endswith(';'):
            s += ';'
        return s

    def visit_Return(self, node):
        if node.value:
            return 'return {};'.format(self.visit(node.value))
        return 'return undefined;'

    def visit_Compare(self, node):
        def merge(a, b, c):
            if a and b:
                c.append(self.visit(a[0]))
                c.append(self.visit(b[0]))
                return merge(a[1:], b[1:], c)
            else:
                return c
        ops = merge(node.ops, node.comparators, [self.visit(node.left)])

        iter = reversed(ops)
        c = next(iter)
        for op in iter:
            c = '({} {} {})'.format(next(iter), op, c)
        return c

    def visit_BoolOp(self, node):
        op = self.visit(node.op)
        return '({})'.format(op.join([self.visit(v) for v in node.values]))

    def visit_If(self, node):
        test = self.visit(node.test)
        body = '\n'.join(map(self.visit, node.body)) + '\n'
        if node.orelse:
            orelse = '\n'.join(map(self.visit, node.orelse)) + '\n'
            return 'if({}) {{\n{}}}\nelse {{\n{}}}\n'.format(test, body, orelse)
        else:
            return 'if({}) {{\n{}}}\n'.format(test, body)

    def visit_Dict(self, node):
        a = []
        for i in range(len(node.keys)):
            k = self.visit(node.keys[i])
            v = self.visit(node.values[i])
            a.append('{}:{}'.format(k, v))
        b = ','.join(a)
        return '{{{}}}'.format(b)

    def visit_For(self, node):
        # support only arrays
        target = node.target.id 
        iterator_index = target + '_iterator_index'
        iterator = self.visit(node.iter) # iter is the python iterator
        iterator_name = 'iterator_{}'.format(target)
        pre_for = 'var {} = {};\n'.format(iterator_name, iterator)
        # replace the replace target with the javascript iterator
        body = 'var {} = {}[{}];\n'.format(target, iterator_name, iterator_index)
        body += '\n'.join(map(self.visit, node.body)) + '\n'
        for_block = pre_for 
        for_block += 'for (var {}=0; {} < {}.length; {}++) {{\n{}}}\n'.format(iterator_index, iterator_index, iterator_name, iterator_index, body)
        return for_block

    def visit_Continue(self, node):
        return 'continue'

    def visit_Lambda(self, node):
        args = ', '.join(map(self.visit, node.args.args))
        return '(function ({}) {{{}}})'.format(args, self.visit(node.body))

    def visit_ClassDef(self, node):
        # 'name', 'bases', 'keywords', 'starargs', 'kwargs', 'body', 'decorator_lis't
        if len(node.bases) > 1:
            raise NotImplemented
        name = node.name
        if len(node.bases) == 0:
            out = 'var {} = Class.$extend({{\n'.format(name)
        else:
            base = self.visit(node.bases[0])
            out = 'var {} = {}.$extend({{\n'.format(name, base)
        self.in_classdef = name
        for node in node.body:
            out += self.visit(node)
        out += '});\n'
        self.in_classdef = None
        return out


def generate_js(filepath, requirejs=False, root_path=None, output=None, deep=None):
    dirname = os.path.abspath(os.path.dirname(filepath))
    if not root_path:
        root_path = dirname
    basename = os.path.basename(filepath)
    output_name = os.path.join(dirname, basename + '.js')
    if not output:
        print('Generating {}'.format(output_name))
    # generate js
    with open(os.path.join(dirname, basename)) as f:
        input = parse(f.read())
    tree = parse(input)
    python_core = PythoniumCore()
    script = python_core.visit(tree)
    if requirejs:
        out = 'define(function(require) {\n'
        out += script
        if isinstance(python_core.__all__, str):
            out += '\nreturn {};\n'.format(python_core.__all__)
        elif python_core.__all__:
            public = '{{{}}}'.format(', '.join(map(lambda x: '{}: {}'.format(x[0], x[1]), zip(python_core.__all__, python_core.__all__))))
            out += '\nreturn {};\n'.format(public)
        else:
            raise Exception('__all__ is not defined!')
        out += '\n})\n'
        script = out
    if deep:
        for dependency in python_core.dependencies:
            if dependency.startswith('.'):
                generate_js(os.path.join(dirname, dependency + '.py'), requirejs, root_path, output, deep)
            else:
                generate_js(os.path.join(root_path, dependency[1:] + '.py'), requirejs, root_path, output, deep)
    output.write(script)


def main():
    from docopt import docopt
    args = docopt(__doc__, version='pythonium_core ' + __version__)
    requirejs = args['--requirejs']
    filepaths = args['FILE']
    output = args['--output']
    if output is None:
        output = sys.stdout
    else:
        output = open(output, 'w')
    deep = args['--deep']
    for filepath in filepaths:
        generate_js(filepath, requirejs, None, output, deep)
    if output:
        output.close()

if __name__ == '__main__':
    main()
