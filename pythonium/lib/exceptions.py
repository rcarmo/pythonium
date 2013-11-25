class Exception:
    
    def __init__(self, message):
        self.message = message


class TypeError(Exception):
    pass


class AttributeError(Exception):
    pass
