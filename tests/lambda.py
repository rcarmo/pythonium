def func(x, y, arg, kwargs):
    return x + y + arg[0] + arg[1] + kwargs["key"]
f = lambda x, y, *args, **kwargs: func(x, y, args, kwargs) + 1
print f(42, 1337, 11, 100, key="value")
