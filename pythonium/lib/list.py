class list:
    
    def __init__(self, jsobject=None):
        if None is jsobject:
            self.jsobject = JSArray()
        else:
            self.jsobject = jsobject

    def append(self, item):
        self.jsobject.push(item)

    def insert(self, index, item):
        self.jsobject.splice(index, 0, item)

    def __len__(self):
        return self.jsobject.length

    def __setitem__(self, index, value):
        jsobject = self.jsobject
        index = index.jsobject
        JS('jsobject[index] = value')

    def __getitem__(self, s):
        jsobject = self.jsobject
        index = s.jsobject
        return JS('jsobject[index]')
        
