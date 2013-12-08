class str:

    def __init__(self, jsobject):
        self.jsobject = jsobject

    def __repr__(self):
        return self

    def __jstype__(self):
        return self.jsobject

    def __hash__(self):
        return '"' + self

    def __contains__(self, s):
        if int(self.jsobject.indexOf(jstype(s))) != -1:
            return True
        return False

    def __iter__(self):
        return ListIterator(self)

    def join(self, objects):
        L = len(objects)
        if not L:
            return ""
        out = objects[0]
        index = 1
        while index < L:
            obj = objects[index]
            out = out + self + obj
            index += 1
        return out

    def __add__(self, other):
        a = self.jsobject
        b = other.jsobject
        return str(jscode('a + b'))

    def __len__(self):
        return int(self.jsobject.length)

    def __lte__(self, other):
        a = self.jsobject
        b = other.jsobject
        if jscode('a <= b'):
            return True
        return False

    def __gte__(self, other):
        a = self.jsobject
        b = other.jsobject
        if jscode('a >= b'):
            return True
        return False

    def __gt__(self, other):
        a = self.jsobject
        b = other.jsobject
        if jscode('a > b'):
            return True
        return False

    def __eq__(self, other):
        a = self.jsobject
        b = other.jsobject
        if jscode('a == b'):
            return True
        return False
        
    def __getitem__(self, index):
        jsobject = self.jsobject
        index = index.jsobject
        c = jscode('jsobject[index]')
        return str(c)

    def __neq__(self, other):
        return not self.__eq__(other)
