def func(a, b, c, d=1, f=2, *args, **kwargs):
    print(a)
    a = 1
    print(a, b, c, d, f)
    print(args[0])
    print(args[1])
    print(kwargs)

kwargs = {"foo": "bar"}
func(42, 43, 44, 45, 46, 100, 102, key="value", **kwargs)
    
