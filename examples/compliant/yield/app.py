tosend = list()
todos = list()


def asyncronous_fetch_one():
    yield 10


def asyncronous_fetch_two():
    yield 32


def main():
    a = yield asyncronous_fetch_one()
    b = yield asyncronous_fetch_two()
    print(a+b)


# bootstrap
tosend.append((main(), None))

print('starting ;)')
while tosend or todos:
    print(tosend, todos)
    while tosend:
        print('in tosend')
        to, value = tosend.pop()
        try:
            n = to.send(value)
        except StopIteration:
            print('fuuuu')
            pass
        else:
            todos.append((to, n))
    while todos:
        print('in todos')
        to, generator = todos.pop()
        try:
            tosend.append((to, next(generator)))
        except StopIteration:
            pass
        else:
            todos.append((to, generator))
        
