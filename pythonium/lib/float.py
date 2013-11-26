class float:

    def __init__(self, jsobject):
        self.jsobject = jsobject
    
    def __div__(self, other):
        a = self.jsobject
        b = other.jsobject
        return float(JS('a / b'))
