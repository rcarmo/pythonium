class dict:
    # only support str, int, float as keys

    def __init__(self, jsobject):
        self.jsobject = jsobject

    def __repr__(self):
        out = []
        for key in self.keys():
            key_repr = repr(key)
            value_repr = repr(self.get(key))
            out.append(key_repr + ': ' + value_repr)
        return "{" + ", ".join(out) + "}"

    def get(self, key, d=None):
        jsobject = self.jsobject
        key = key.jsobject
        attr = JS('jsobject[key]')
        if None is not attr:
            return attr
        else:
            return d

    def __setitem__(self, key, value):
        self.jsobject[key] = value

    def keys(self):
        return map(str, list(Object.keys(self.jsobject)))

    def items(self):
        out = list()
        for key in self.keys():
            out.append([key, self.get(key)])
        return out
