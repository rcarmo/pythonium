def func():
    index = 0
    while index < 3:
        yield index
        index += 1

gen = func()
print(next(gen))
print(next(gen))
print(next(gen))
