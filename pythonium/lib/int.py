class int:

    def __init__(self, jsobject):
        self.jsobject = jsobject

    def __repr__(self):
        return self

    def __add__(self, other):
        a = self.jsobject
        b = other.jsobject
        return int(JS('a + b'))

    def __sub__(self, other):
        a = self.jsobject
        b = other.jsobject
        return int(JS('a - b'))

    def __lt__(self, other):
        a = self.jsobject
        b = other.jsobject
        if JS('a < b'):
            return True
        return False

    def __lte__(self, other):
        a = self.jsobject
        b = other.jsobject
        if JS('a <= b'):
            return True
        return False

    def __mul__(self, other):
        a = self.jsobject
        b = other.jsobject
        c = JS('a * b')
        return int(c)

    def __or__(self, other):
        a = self.jsobject
        b = other.jsobject
        c = JS('a || b')
        return int(c)

    def __eq__(self, other):
        a = self.jsobject
        b = other.jsobject
        if JS('a == b'):
            return True
        return False

    def __neg__(self):
        jsobject = self.jsobject
        return int(JS('-jsobject'))

    def __div__(self, other):
        a = self.jsobject
        b = other.jsobject
        return int(JS('a / b'))
