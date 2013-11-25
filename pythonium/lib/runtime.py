object = {__bases__: [], __name__: 'object'}
object.__mro__ = [object]

type = {__bases__: [object], __mro__: [object], __name__:'type'}

object.__metaclass__ = type


def issubclass(klass, other):  
    if klass is other:
        return True
    if not klass.__bases__:
        return False
    for base in klass.__bases__:
        if issubclass(base, other):
            return True
    return False


def isinstance(object, klass):
    if object.__class__:
        return issubclass(object.__class__, klass)
    return False


def pythonium_call(object):
    args = Array.prototype.slice.call(arguments, 1)
    if object.__metaclass__:
        instance = {__class__: object}
        init = pythonium_get_attribute(instance, '__init__')
        init(args)
        return instance
    else:
        return object.apply(object, args)



def pythonium_mro(bases):
    """Calculate the Method Resolution Order of bases using the C3 algorithm.

    Suppose you intended creating a class K with the given base classes. This
    function returns the MRO which K would have, *excluding* K itself (since
    it doesn't yet exist), as if you had actually created the class.

    Another way of looking at this, if you pass a single class K, this will
    return the linearization of K (the MRO of K, *including* itself).
    """
    # based on http://code.activestate.com/recipes/577748-calculate-the-mro-of-a-class/
    seqs = [C.__mro__ for C in bases]
    seqs.push(bases.slice())
    res = []
    while True:
        # non_empty = list(filter(None, seqs))
        non_empty = []
        for seq in seqs:
            empty = True
            for item in seq:
                if item:
                    empty = False
                    break
            if not empty:
                non_empty.push(seq)
        if non_empty.length == 0:
            # Nothing left to process, we're done.
            return res
        for seq in non_empty:  # Find merge candidates among seq heads.
            candidate = seq[0]
            not_head = [s for s in non_empty if candidate in s.splice(1)]
            if not_head.length != 0:
                # Reject the candidate.
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
    attrs.__metaclass__ = type
    attrs.__bases__ = bases
    mro = pythonium_mro(bases)
    mro.splice(0, 0, attrs)
    attrs.__mro__ = mro
    return attrs


def pythonium_get_attribute(object, attr, look_for_getattr=True):
    if object.__class__:
        object_attr = object[attr]
        if object_attr:
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
                if class_attr:
                    if {}.toString.call(class_attr) == '[object Function]':
                        def method_wrapper():
                            args = Array.prototype.slice.call(arguments)
                            args.splice(0, 0, object)
                            return class_attr.apply(None, args)
                        return method_wrapper
                    return class_attr
    attr = object[attr]
    if attr:
        if {}.toString.call(attr) == '[object Function]':
            def method_wrapper():
                return attr.apply(object, arguments)
            return method_wrapper
        else:
            return attr
    raise AttributeError


def pythonium_set_attribute(object, attr, value):
    object[attr] = value
