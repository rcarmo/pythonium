class int:

    def __init__(self, jsobject):
        self.jsobject = jsobject

    def __add__(self, other):
        a = self.jsobject
        b = other.jsobject
        return int(JS('a + b'))

    def __lt__(self, other):
        a = self.jsobject
        b = other.jsobject
        return JS('a < b')
