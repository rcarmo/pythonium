def range(a, b=None):
    if b:
        index = a
        end = b
    else:
        index = 0
        end = a
    out = list()
    while index < end:
        out.append(index)
        index += 1
    return out


def repr(obj):
    return obj.__repr__()


def print(*args):
    out = JSArray()
    for arg in args:
        out.push(jstype(repr(arg)))
    jscode('console.log.apply(console, out)')


def map(func, objects):
    out = list()
    for obj in objects:
        out.append(func(obj))
    return out


def jstype(obj):
    return obj.__jstype__()


def hash(obj):
    return obj.__hash__()


def iter(obj):
    return obj.__iter__()


def next(obj):
    if jscode('obj.next !== undefined'):
        r = jscode('obj.next()')
        if jscode('r.done'):
            raise StopIteration
        else:
            return jscode('r.value')
    return obj.__next__()


def len(obj):
    return obj.__len__()


def abs(obj):
    return obj.__abs__()


def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True


def any(iterable):
    for element in iterable:
        if element:
            return True
    return False


def callable(obj):
    if jscode("Object.toString.call(obj) ==='[object Function]'"):
        return True
    if jscode('obj.next'):
        return True
    if obj.__class__:
        return True
    if jscode("lookup(obj, '__call__')"):
        return True
    return False


def classmethod(func):
    func.classmethod = True
    return func


def staticmethod(func):
    func.staticmethod = True
    return func


class enumerate:

    def __init__(self, iterator):
        self.iterator = iterator
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        return (index, next(self.iterator)
