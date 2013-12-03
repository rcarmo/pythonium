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
    out = list()
    for arg in args:
        r = repr(arg)  # returns a str object
        out.append(r.jsobject)
    console.log.apply(console, out.jsobject)


def map(func, objects):
    out = list()
    for obj in objects:
        out.append(func(obj))
    return out

def jstype(obj):
    # XXX: fallback to __jstype__ method when it doesn't exist
    return obj.jsobject
