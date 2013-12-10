class A:

    def __init__(self):
        self.jsobject = jscode('"Héllo"')
        console.log(self.jsobject.length)

A()
