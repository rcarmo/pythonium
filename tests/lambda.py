def func(x, y, arg, kwargs):
    print(x)
    print(y)
    print(arg[0])
    print(arg[1])
    print(kwargs["key"])
x = lambda x, y, *args, **kwargs: func(x, y, args, kwargs)
x(42, 1337, 11, 100, key="value")
