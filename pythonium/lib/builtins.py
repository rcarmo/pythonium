def filter(func, objects):
    if func:
        def generator():
            for obj in objects:
                if func(obj):
                    yield obj
    else:
        def generator():
            for obj in objects:
                if obj:
                    yield obj
    return Generator(generator)
