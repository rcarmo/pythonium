class dict:

    def __init__(self, jsobject=None):
        # Since JavaScript objects can only have string as keys
        # storing the original object keys is needed
        # to be able to answer the ``dict.keys`` and other methods
        if jsobject:
            self.keys = map(str, list(Object.keys(self.jsobject)))
            self.jsobject = JSObject()
        else:
            self.keys = list()
            self.jsobject = JSObject()

    def __hash__(self):
        raise TypeError("unhashable type: 'dict'")

    def __jstype__(self):
        raise NotImplementedError

    def __repr__(self):
        out = []
        for key in self.keys():
            key_repr = repr(key)
            value_repr = repr(self[key])
            out.append(key_repr + ': ' + value_repr)
        return "{" + ", ".join(out) + "}"

    def get(self, key, d=None):
        if key in self.keys:
            h = jstype(hash(key))
            jsobject = self.jsobject
            return JS('jsobject[h]')
        return d

    def __getitem__(self, key):
        if key in self.keys:
            h = jstype(hash(key))
            jsobject = self.jsobject
            return JS('jsobject[h]')
        raise KeyError(key)

    def __setitem__(self, key, value):
        h = jstype(hash(key))
        jsobject = self.jsobject
        JS('jsobject[h] = value')
        self.keys.append(key)

    def keys(self):
        return self.keys

    def items(self):
        out = list()
        for key in self.keys():
            out.append([key, self[key]])
        return out
