class str:

    def __init__(self, jsobject):
        self.jsobject = jsobject

    def __add__(self, other):
        a = self.jsobject
        b = other.jsobject
        return str(JS('a + b'))

        
