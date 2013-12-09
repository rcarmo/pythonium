x = lambda x, y, *args, **kwargs: print(x, y, args, kwargs)
x(42, 1337, 11, 100, key="value")
