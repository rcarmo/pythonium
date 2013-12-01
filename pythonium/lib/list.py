class StopIteration:
    pass


def iter(obj):
    return obj.__iter__()


def next(obj):
    return obj.__next__()


def len(obj):
    return obj.__len__()


class ListIterator:

    def __init__(self, obj):
        self.list = obj
        self.index = 0
        self.length = len(obj)

    def __next__(self):
        if self.index == self.length:
            raise StopIteration
        self.index = self.index + 1
        return self.list[self.index - 1]


class list:
    
    def __init__(self, jsobject=None):
        if jsobject:
            self.jsobject = jsobject
        else:
            self.jsobject = JSArray()

    def append(self, item):
        jsobject = self.jsobject
        JS('jsobject.push(item)')

    def insert(self, index, item):
        self.jsobject.splice(index, 0, item)

    def __setitem__(self, index, value):
        jsobject = self.jsobject
        index = index.jsobject
        JS('jsobject[index] = value')

    def __getitem__(self, s):
        jsobject = self.jsobject
        index = s.jsobject
        return JS('jsobject[index]')

    def __len__(self):
        jsobject = self.jsobject
        length = JS('jsobject.length')
        return int(length)

    def __iter__(self):
        return ListIterator(self)
