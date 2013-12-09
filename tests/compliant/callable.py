print(callable(abs))
print(callable(int))
print(callable(True))
print(callable(bool))

class GenerateCallable:

    def __call__(self):
        return 42

print(callable(GenerateCallable))
print(callable(GenerateCallable()))

class GenerateNonCallable:
    pass

print(callable(GenerateNonCallable))
print(callable(GenerateNonCallable()))


def generator():
    yield 42

print(callable(generator))
print(callable(generator()))
