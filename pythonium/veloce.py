import os
import sys
from io import StringIO

from ast import Str
from ast import Name
from ast import List
from ast import Tuple
from ast import parse
from ast import Assign
from ast import Global
from ast import FunctionDef
from ast import NodeVisitor


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


class Veloce(NodeVisitor):

    def __init__(self):
        super().__init__()
        self.dependencies = []
        self.in_classdef = None
        self._function_stack = []
        self.__all__ = None
        self.writer = Writer()
        self._uuid = -1

    def uuid(self):
        self._uuid += 1
        return self._uuid

    def visit(self, node):
        if os.environ.get('DEBUG', False):
            print(">>>", node.__class__.__name__, node._fields)
        return super().visit(node)

    def visit_Pass(self, node):
        self.writer.write('/* pass */')

    def visit_Try(self, node):
        self.writer.write('try {')
        self.writer.push()
        list(map(self.visit, node.body))
        self.writer.pull()
        self.writer.write('}')
        self.writer.write('catch(__exception__) {')
        self.writer.push()
        list(map(self.visit, node.handlers))
        self.writer.pull()
        self.writer.write('}')

    def visit_Raise(self, node):
        self.writer.write('throw {};'.format(self.visit(node.exc)))

    def visit_ExceptHandler(self, node):
        list(map(self.visit, node.body))

    def visit_Yield(self, node):
        self.writer.write('yield {};'.format(self.visit(node.value)))

    def visit_In(self, node):
        return ' in '

    def visit_Module(self, node):
        list(map(self.visit, node.body))

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
            self.writer.write('var {} = require("{}");'.format(asname, path))
            self.dependencies.append('/' + path)  # relative to project root
        elif node.level == 1:
            self.writer.write('var {} = require.toUrl("./{}");'.format(asname, path))
            self.dependencies.append('./' + path)  # relative to current file
        else:
            path = '../' * node.level + path
            self.writer.write('var {} = require.toUrl("{}");'.format(asname, path))
            self.dependencies.append(path)  # relative to current file
        return out

    def visit_Global(self, node):
        # handled in visit_FunctionDef
        return ''

    def visit_FunctionDef(self, node):
        # 'name', 'args', 'body', 'decorator_list', 'returns'
        self._function_stack.append(node.name)
        args, kwargs, varargs, varkwargs = self.visit(node.args)

        all_parameters = list(args)
        all_parameters.extend(kwargs.keys())
        if varargs:
            all_parameters.append(varargs)
        if varkwargs:
            all_parameters.append(varkwargs)
        all_parameters = set(all_parameters)

        if self.in_classdef and len(self._function_stack) == 1:
            __args = ', '.join(args[1:])
            self.writer.write('{}: function({}) {{'.format(node.name, __args))
        else:
            __args = ', '.join(args)
            self.writer.write('var {} = function({}) {{'.format(node.name, __args))
        self.writer.push()
        if not varkwargs:
            varkwargs = '__kwargs'

        # unpack arguments
        self.writer.write('var __args = Array.prototype.slice.call(arguments);')
        self.writer.write('var {} = __args[__args.length - 1];'.format(varkwargs))
        for keyword in kwargs.keys():
            self.writer.write('{} = {} || {}.{} || {};'.format(keyword, keyword, varkwargs, keyword, kwargs[keyword]))
            self.writer.write('delete {}.{};'.format(varkwargs, keyword))
        if varargs:
            self.writer.write('var {} = __args.splice({});'.format(varargs, len(args)))
            self.writer.write('{}.pop();'.format(varargs))
        # check for variable creation use var if not global
        def retrieve_vars(body, vars=None):
            local_vars = set()
            global_vars = vars if vars else set()
            for n in body:
                if isinstance(n, Assign) and isinstance(n.targets[0], Name):
                    local_vars.add(n.targets[0].id)
                elif isinstance(n, Assign) and isinstance(n.targets[0], Tuple):
                    for target in n.targets:
                        for target in target.elts:
                            local_vars.add(target.id)
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

        local_vars, global_vars = retrieve_vars(node.body, all_parameters)

        if local_vars - global_vars:
            a = ','.join(local_vars-global_vars)
            self.writer.write('var {};'.format(a))

        # output function body
        list(map(self.visit, node.body))
        self.writer.pull()
        if self.in_classdef and len(self._function_stack) == 1:
            self.writer.write('},')
        else:
            self.writer.write('};')

        for decorator in node.decorator_list:
            decorator = self.visit(decorator)
            self.writer.write('{} = {}({});'.format(node.name, decorator, node.name))
        self._function_stack.pop()

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
        attr = node.attr.replace('__DOLLAR__', '$')
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
            s = 'console.log({})'.format(', '.join(args))
            return s
        else:
            if node.args:
                args = [self.visit(e) for e in node.args]
                args = [e for e in args if e]
            else:
                args = []
            if node.keywords and not node.kwargs:
                keywords = '__kwargs{}__'.format(self.uuid())
                _ = ', '.join(map(lambda x: '{}: {}'.format(x[0], x[1]), map(self.visit, node.keywords)))
                self.writer.write('var {} = {{{}}}'.format(keywords, _))
                args.append(keywords)
            elif node.kwargs and not node.keywords:
                args.append(node.kwargs.id)
            elif node.kwargs and node.keywords:
                for key, value in map(self.visit, node.keywords):
                    self.writer.write('{}.{} = {}'.format(node.kwargs.id, key, value))
                args.append(node.kwargs.id)
            return '{}({})'.format(name, ', '.join(args))

    def visit_ListComp(self, node):
        # 'elt', 'generators'
        comprehension = '__comp{}__'.format(self.uuid())
        self.writer.write('var {} = [];'.format(comprehension))
        list(map(self.visit, node.generators))
        value = self.visit(node.elt)
        self.writer.write('{}.push({});'.format(comprehension, value))
        for _ in node.generators:
            self.writer.pull()
            self.writer.write('}')
        return comprehension

    def visit_comprehension(self, node):
        # 'target', 'iter', 'ifs'
        iterator = '__iterator{}__'.format(self.uuid())
        index = '__index{}__'.format(self.uuid())
        self.writer.write('var {} = {};'.format(iterator, self.visit(node.iter)))
        self.writer.write('for (var {} = 0; {}<{}.length; {}++) {{'.format(index, index, iterator, index))
        self.writer.push()
        self.writer.write('var {} = {}[{}];'.format(self.visit(node.target), iterator, index))
        if node.ifs:
            self.writer.write('if(!{}) {{ continue; }}'.format(' && '.join(map(self.visit, node.ifs))))

    def visit_While(self, node):
        self.writer.write('while({}) {{'.format(node.test))
        list(map(self.visit, node.body))

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        self.writer.write('{} = {} {} {};'.format(target, target, self.visit(node.op), self.visit(node.value)))

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
        target = node.targets[0]
        value = self.visit(node.value)
        self.writer.write('var __assignement = {};'.format(value))
        for target in node.targets:
            if isinstance(target, Tuple):
                targets = map(self.visit, target.elts)
                for index, target in enumerate(targets):
                    self.writer.write('{} = __assignement[{}];\n'.format(target, index))
            else:
                target = self.visit(target)
                if self.in_classdef and len(self._function_stack) == 0:
                    self.writer.write('{}: {},'.format(target, value))
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
                    else:
                        self.writer.write('{} = __assignement;'.format(target))

    def visit_Expr(self, node):
        self.writer.write(self.visit(node.value) + ';')

    def visit_Return(self, node):
        if node.value:
            self.writer.write('return {};'.format(self.visit(node.value)))

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
        self.writer.write('if({}) {{'.format(test))
        self.writer.push()
        list(map(self.visit, node.body))
        self.writer.pull()
        self.writer.write('}')
        if node.orelse:
            self.writer.write('else {')
            self.writer.push()
            list(map(self.visit, node.orelse))
            self.writer.pull()
            self.writer.write('}')

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
        self.writer.write('var {} = {};'.format(iterator_name, iterator))
        # replace the replace target with the javascript iterator
        self.writer.write('for (var {}=0; {} < {}.length; {}++) {{'.format(iterator_index, iterator_index, iterator_name, iterator_index))
        self.writer.push()
        self.writer.write('var {} = {}[{}];'.format(target, iterator_name, iterator_index))
        list(map(self.visit, node.body))
        self.writer.pull()
        self.writer.write('}')

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
            self.writer.write('var {} = Class.$extend({{'.format(name))
        else:
            base = self.visit(node.bases[0])
            self.writer.write('var {} = {}.$extend({{'.format(name, base))
        self.writer.push()
        self.in_classdef = name
        list(map(self.visit, node.body))
        self.writer.pull()
        self.writer.write('});')
        self.in_classdef = None


def veloce_generate_js(filepath, requirejs=False, root_path=None, output=None, deep=None):
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
    python_core = Veloce()
    python_core.visit(tree)
    script = python_core.writer.value()
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
