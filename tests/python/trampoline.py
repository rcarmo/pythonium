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


def trampoline():
    requestAnimationFrame(trampoline)
    while tosend or todos:
        while tosend:
            to, value = tosend.pop()
            try:
                new = to.send(value)
            except StopIteration:
                pass
            else:
                todos.append((to, new))
        while todos:
            to, generator = todos.pop()
            try:
                tosend.append((to, next(generator)))
            except StopIteration:
                pass
            else:
                todos.append((to, generator))


trampoline()
