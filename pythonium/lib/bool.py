class _True:

    def __init__(self):
        self.jsobject = JS('true')

    def __and__(self, other):
        if JS('other === self'):
            return True
        return False

    def __or__(self, other):
        return True

    def __is__(self, other):
        if JS('other === self'):
            return True
        return False

    def __neg__(self):
        return False


class _False:

    def __init__(self):
        self.jsobject = JS('false')

    def __and__(self, other):
        return False

    def __or__(self, other):
        if JS('other === True'):
            return True
        return False

    def __is__(self, other):
        if JS('other === self'):
            return True
        return False

    def __neg__(self):
        return True


__TRUE = _True()
__FALSE = _False()
