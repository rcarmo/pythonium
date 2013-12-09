__object = {__bases__: [], __name__: 'object'}
__object.__mro__ = [__object]

__type = {__bases__: [__object], __mro__: [__object], __name__: 'type'}

__object.__metaclass__ = __type


__ARGUMENTS_PADDING__ = {ARGUMENTS_PADDING: "YES IT IS!"}


def __is__(self, other):
    return (self is other)
__object.__is__ = __is__

def __isnot__(self, other):
    return not (self is other)
__object.__isnot__ = __isnot__


def __hash__(me):
    uid = lookup(me, 'uid')
    if not uid:
        uid = __object._uid
        __object._uid += 1
        self.__uid__ = uid
    return pythonium_call(str, '{' + uid)
__object._uid = 1
__object.__hash__ = __hash__


def __rcontains__(me, other):
    contains = lookup(other, '__contains__')
    return contains(me)
__object.__rcontains__ = __rcontains__;


def issubclass(klass, other):  
    if klass is other:
        return True
    if not klass.__bases__:
        return False
    for base in klass.__bases__:
        if issubclass(base, other):
            return True
    return False


def pythonium_is_true(v):
    if v is False:
        return False
    if v is True:
        return True
    if v is __NONE:
        return False
    if v is __FALSE:
        return False
    if isinstance(v, int) or isinstance(v, float):
        if v.jsobject == 0:
            return False
    length = lookup(v, '__length__')
    if length and length() == 0:
        return False
    return True


def isinstance(object, klass):
    if object.__class__:
        return issubclass(object.__class__, klass)
    return False

def pythonium_obj_to_js_exception(obj):
    def exception():
        this.exception = obj
    return exception


def pythonium_is_exception(obj, exc):
    if obj is exc:
        return True
    return isinstance(obj, exc)


def pythonium_call(object):
    args = Array.prototype.slice.call(arguments, 1)
    if object.__metaclass__:
        instance = {__class__: object}
        init = lookup(instance, '__init__')
        if init:
            init.apply(instance, args)
        return instance
    else:
        return object.apply(object, args)

def pythonium_create_empty_dict():
    instance = {__class__: dict}
    instance._keys = pythonium_call(list)
    instance.jsobject = JSObject()
    return instance
  

def pythonium_mro(bases):
    """Calculate the Method Resolution Order of bases using the C3 algorithm.

    Suppose you intended creating a class K with the given base classes. This
    function returns the MRO which K would have, *excluding* K itself (since
    it doesn't yet exist), as if you had actually created the class.

    Another way of looking at this, if you pass a single class K, this will
    return the linearization of K (the MRO of K, *including* itself).
    """
    # based on http://code.activestate.com/recipes/577748-calculate-the-mro-of-a-class/
    seqs = [C.__mro__.slice() for C in bases]
    seqs.push(bases.slice())

    def cdr(l):
        l = l.slice()
        l = l.splice(1)
        return l
    res = []
    while True:
        non_empty = []
        for seq in seqs:
            empty = True
            out = []
            for item in seq:
                if item:
                    empty = False
                    out.push(item)
            if not empty:
                non_empty.push(out)
        if non_empty.length == 0:
            # Nothing left to process, we're done.
            return res
        for seq in non_empty:  # Find merge candidates among seq heads.
            candidate = seq[0]
            not_head = []
            for s in non_empty:
                if candidate in cdr(s):
                    not_head.push(s)
            if not_head.length != 0:
                candidate = None
            else:
                break
        if not candidate:
            raise TypeError("Inconsistent hierarchy, no C3 MRO is possible")
        res.push(candidate)
        for seq in seqs:
            # Remove candidate.
            index = seq.indexOf(candidate)
            if index >= 0:
                del seq[index]


def pythonium_create_class(name, bases, attrs):
    attrs.__name__ = name
    attrs.__metaclass__ = __type
    attrs.__bases__ = bases
    mro = pythonium_mro(bases)
    mro.splice(0, 0, attrs)
    attrs.__mro__ = mro
    return attrs


def lookup(object, attr):
    object_attr = object[attr]
    if object_attr != None:
        if object_attr and {}.toString.call(object_attr) == '[object Function]':
            def method_wrapper():
                args = Array.prototype.slice.call(arguments)
                args.splice(0, 0, object)
                return object_attr.apply(None, args)
            return method_wrapper
        return object_attr
    else:
        for base in object.__class__.__mro__:
            class_attr = base[attr]
            if class_attr != None:
                if {}.toString.call(class_attr) == '[object Function]':
                    def method_wrapper():
                        args = Array.prototype.slice.call(arguments)
                        args.splice(0, 0, object)
                        return class_attr.apply(None, args)
                    return method_wrapper
                return class_attr


def pythonium_object_get_attribute(object, attr):
    r = lookup(object, attr)
    if r != None:
        return r
    else:
        getattr = lookup(object, '__getattr__')
        if getattr:
            return getattr(attr)
        else:
            console.trace('AttributeError', attr, object)
            raise AttributeError

__object.__getattribute__ = pythonium_object_get_attribute


def pythonium_get_attribute(object, attr):
    if object.__class__:
        getattribute = lookup(object, '__getattribute__')
        return getattribute(attr)
    attr = object[attr]
    if attr:
        if {}.toString.call(attr) == '[object Function]':
            def method_wrapper():
                return attr.apply(object, arguments)
            return method_wrapper
        else:
            return attr


def pythonium_set_attribute(object, attr, value):
    object[attr] = value


def ASSERT(condition, message):
    if not condition:
        raise message or pythonium_call(str, 'Assertion failed')
