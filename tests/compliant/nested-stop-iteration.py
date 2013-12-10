try:
    for i in range(10):
        next(iter(list()))
except:
    print('catch!')

try:
    for i in range(10):
        next(iter(list()))
except StopIteration:
    print('catch!')
