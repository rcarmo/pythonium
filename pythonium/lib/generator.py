class Generator:

    def __init__(self, generator):
        self.generator = generator

    def next(self):
        try:
            return self.generator.next()
        except:
            if {}.toString.call(__exception__) == '[object StopIteration]':
                raise StopIteration
            else:
                raise Exception(__exception__)
