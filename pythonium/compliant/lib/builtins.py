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
    return obj.__next__()


def len(obj):
    return obj.__len__()



