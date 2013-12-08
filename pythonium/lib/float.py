class float:

    def __init__(self, jsobject):
        self.jsobject = jsobject

    def __hash__(self):
        return str(self.jsobject)

    def __repr__(self):
        return self
    
    def __div__(self, other):
        a = self.jsobject
        b = other.jsobject
        return float(JS('a / b'))

    def __sub__(self, other):
        a = self.jsobject
        b = other.jsobject
        return float(JS('a - b'))

    def __eq__(self, other):
        a = self.jsobject
        b = other.jsobject
        if JS('a == b'):
            return True
        return False
