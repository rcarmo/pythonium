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
    
    def __init__(self):
        self.jsobject = JSArray()

    def __hash__(self):
        raise TypeError("unhashable type: 'list'")

    def __repr__(self):
        return "[" + ", ".join(map(repr, self)) + "]"

    def __jstype__(self):
        out = JSArray()
        for item in self:
            item = jstype(item)
            jscode('out.push(item)')
        return out

    def append(self, item):
        jsobject = self.jsobject
        jscode('jsobject.push(item)')

    def insert(self, index, item):
        self.jsobject.splice(index, 0, item)

    def __setitem__(self, index, value):
        jsobject = self.jsobject
        index = index.jsobject
        jscode('jsobject[index] = value')

    def __getitem__(self, s):
        jsobject = self.jsobject
        index = jstype(s)
        return jscode('jsobject[index]')

    def __len__(self):
        jsobject = self.jsobject
        length = jscode('jsobject.length')
        return int(length)

    def __iter__(self):
        return ListIterator(self)

    def __contains__(self, obj):
        for item in self:
            if obj == item:
                return True
        return False
            
