class dict:

    def __init__(self, jsobject):
        self.jsobject = jsobject

    def get(self, key, d=None):
        attr = self.jsobject[key]
        if attr:
            return attr
        else:
            return d

    def __setitem__(self, key, value):
        self.jsobject[key] = value

    def keys(self):
        return list(Object.keys(self.jsobject))
