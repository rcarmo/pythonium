class list:
    
    def __init__(self, jsobject=None):
        if isinstance(jsobject, Generator):
            self.jsobject = JSArray()
            for item in jsobject:
                self.jsobject.push(item)
        elif jsobject:
            self.jsobject = jsobject
        else:
            self.jsobject = JSArray()

    def append(self, item):
        self.jsobject.push(item)

    def insert(self, index, item):
        self.jsobject.splice(index, 0, item)

    def __len__(self):
        return self.jsobject.length

    def __getitem__(self, s):
        if isinstance(s, slice):
            out = list()
            index = slice.start
            if slice.end:
                end = slice.end
            else:
                end = len(self)
            if slice.step:
                step = slice.step
            else:
                step = 1
            while index <= end:
                out.append(self[index])
                index += step
            return out
        else:
            return self.jsobject[s]
        
