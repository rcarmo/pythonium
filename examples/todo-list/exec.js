__object = {__bases__:[],__name__:"object"};
__object.__mro__ = [__object];
__type = {__bases__:[__object],__mro__:[__object],__name__:"type"};
__object.__metaclass__ = __type;
__ARGUMENTS_PADDING__ = {ARGUMENTS_PADDING:"YES IT IS!"};
var __isnot__ = function(self, other) {
    return !(this === other);
};
__object.__isnot__ = __isnot__;
var issubclass = function(klass, other) {
    if((klass === other)) {
        return true;
    }
    if(!klass.__bases__) {
        return false;
    }
    var iterator_base = klass.__bases__;
    for (var base_iterator_index=0; base_iterator_index < iterator_base.length; base_iterator_index++) {
        var base = iterator_base[base_iterator_index];
        if(issubclass(base, other)) {
            return true;
        }
    }
    return false;
};
var pythonium_create_dict = function(keys, values) {
    var key,out,index,value,max;
    out = {};
    max = keys.length;
    index = 0;
    while((index < max)) {
        key = keys[index].jsobject;
        value = values[index];
        out[key] = value;
        index = index + 1;
    }
    return pythonium_call(dict, out, undefined);
};
var pythonium_is_true = function(v) {
    if(((v === __FALSE)||(v === false))) {
        return false;
    }
    if(((v === __TRUE)||(v !== undefined&&(v != __NONE)))) {
        return true;
    }
    if(isinstance(v, int)) {
        if((pythonium_get_attribute(v, "jsobject") == 0)) {
            return false;
        }
        return true;
    }
    return false;
};
var isinstance = function(object, klass) {
    if(object.__class__) {
        return issubclass(object.__class__, klass);
    }
    return false;
};
var pythonium_obj_to_js_exception = function(obj) {
    var exception = function() {
        this.exception = obj;
    };
    return exception;
};
var pythonium_is_exception = function(obj, exc) {
    if((obj === exc)) {
        return true;
    }
    return isinstance(obj, exc);
};
var pythonium_call = function(object) {
    var instance,init,args;
    args = Array.prototype.slice.call(arguments, 1);
    if(object.__metaclass__) {
        instance = {__class__:object};
        init = lookup(instance, "__init__");
        if(init) {
            init.apply(instance, args);
        }
        return instance;
    }
    else {
        return object.apply(object, args);
    }
};
var pythonium_mro = function(bases) {
    var not_head,candidate,non_empty,res,empty,index,seqs;
    "Calculate the Method Resolution Order of bases using the C3 algorithm.\n\n    Suppose you intended creating a class K with the given base classes. This\n    function returns the MRO which K would have, *excluding* K itself (since\n    it doesn't yet exist), as if you had actually created the class.\n\n    Another way of looking at this, if you pass a single class K, this will\n    return the linearization of K (the MRO of K, *including* itself).\n    ";
    var __comp0__ = [];
    var __iterator1__ = bases;
    for (var __index2__ = 0; __index2__<__iterator1__.length; __index2__++) {
        var C = __iterator1__[__index2__];
        __comp0__.push(C.__mro__);
    }
    seqs = __comp0__;
    seqs.push(bases.slice());
    res = [];
    while(true) {
        non_empty = [];
        var iterator_seq = seqs;
        for (var seq_iterator_index=0; seq_iterator_index < iterator_seq.length; seq_iterator_index++) {
            var seq = iterator_seq[seq_iterator_index];
            empty = true;
            var iterator_item = seq;
            for (var item_iterator_index=0; item_iterator_index < iterator_item.length; item_iterator_index++) {
                var item = iterator_item[item_iterator_index];
                if(item) {
                    empty = false;
                    break;
                }
            }
            if(!empty) {
                non_empty.push(seq);
            }
        }
        if((non_empty.length == 0)) {
            return res;
        }
        var iterator_seq = non_empty;
        for (var seq_iterator_index=0; seq_iterator_index < iterator_seq.length; seq_iterator_index++) {
            var seq = iterator_seq[seq_iterator_index];
            candidate = seq[0];
            var __comp3__ = [];
            var __iterator4__ = non_empty;
            for (var __index5__ = 0; __index5__<__iterator4__.length; __index5__++) {
                var s = __iterator4__[__index5__];
                if(!(candidate  in  s.splice(1))) { continue; }
                __comp3__.push(s);
            }
            not_head = __comp3__;
            if((not_head.length != 0)) {
                candidate = undefined;
            }
            else {
                break;
            }
        }
        if(!candidate) {
            throw TypeError("Inconsistent hierarchy, no C3 MRO is possible");
        }
        res.push(candidate);
        var iterator_seq = seqs;
        for (var seq_iterator_index=0; seq_iterator_index < iterator_seq.length; seq_iterator_index++) {
            var seq = iterator_seq[seq_iterator_index];
            index = seq.indexOf(candidate);
            if((index >= 0)) {
                delete seq[index];
            }
        }
    }
};
var pythonium_create_class = function(name, bases, attrs) {
    var mro;
    attrs.__name__ = name;
    attrs.__metaclass__ = __type;
    attrs.__bases__ = bases;
    mro = pythonium_mro(bases);
    mro.splice(0, 0, attrs);
    attrs.__mro__ = mro;
    return attrs;
};
var lookup = function(object, attr) {
    var object_attr,class_attr;
    object_attr = object[attr];
    if((object_attr != undefined)) {
        if((object_attr&&({}.toString.call(object_attr) == "[object Function]"))) {
            var method_wrapper = function() {
                var args;
                args = Array.prototype.slice.call(arguments);
                args.splice(0, 0, object);
                return object_attr.apply(undefined, args);
            };
            return method_wrapper;
        }
        return object_attr;
    }
    else {
        var iterator_base = object.__class__.__mro__;
        for (var base_iterator_index=0; base_iterator_index < iterator_base.length; base_iterator_index++) {
            var base = iterator_base[base_iterator_index];
            class_attr = base[attr];
            if((class_attr != undefined)) {
                if(({}.toString.call(class_attr) == "[object Function]")) {
                    var method_wrapper = function() {
                        var args;
                        args = Array.prototype.slice.call(arguments);
                        args.splice(0, 0, object);
                        return class_attr.apply(undefined, args);
                    };
                    return method_wrapper;
                }
                return class_attr;
            }
        }
    }
};
var pythonium_object_get_attribute = function(object, attr) {
    var getattr,r;
    r = lookup(object, attr);
    if((r != undefined)) {
        return r;
    }
    else {
        getattr = lookup(object, "__getattr__");
        if(getattr) {
            return getattr(attr);
        }
        else {
            throw AttributeError;
        }
    }
};
__object.__getattribute__ = pythonium_object_get_attribute;
var pythonium_get_attribute = function(object, attr) {
    var getattribute;
    if(object.__class__) {
        getattribute = lookup(object, "__getattribute__");
        return getattribute(attr);
    }
    attr = object[attr];
    if(attr) {
        if(({}.toString.call(attr) == "[object Function]")) {
            var method_wrapper = function() {
                return attr.apply(object, arguments);
            };
            return method_wrapper;
        }
        else {
            return attr;
        }
    }
};
var pythonium_set_attribute = function(object, attr, value) {
    object[attr] = value;
};
var range = function(a, b) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    if (__args[__args.length - 2] === __ARGUMENTS_PADDING__) {
        var __kwargs = __args[__args.length - 1];
        var varkwargs_start = __args.length - 2;
    } else {
        var __kwargs = {};
        var varkwargs_start = undefined;
    }
    if (varkwargs_start !== undefined && 1 > varkwargs_start) {
        b = __kwargs.b || __NONE;
    } else {
        b = b || __kwargs.b || __NONE;
    }
    /* END unpacking arguments */
    var out,end,index;
    /* BEGIN function */
    if (pythonium_is_true(b)) {
        index = a;
        end = b;
    }
    else {
        index = pythonium_call(int, 0);
        end = a;
    }
    out = pythonium_call(list);
    while(pythonium_is_true((pythonium_get_attribute(index, "__lt__")(end)))) {
        pythonium_call(pythonium_get_attribute(out, "append"), index);
        index = pythonium_call(pythonium_get_attribute(index, "__add__"), pythonium_call(int, 1));
    }
    return out;
};
var repr = function(obj) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call(pythonium_get_attribute(obj, "__repr__"));
};
var print = function() {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    var args = __args.splice(0);
    args = pythonium_call(list, args);
    /* END unpacking arguments */
    var out,r;
    /* BEGIN function */
    out = pythonium_call(list);
    try {
        var __next__ = pythonium_get_attribute(iter(args), "__next__");
        while(true) {
            var arg = pythonium_call(__next__);
            r = pythonium_call(repr, arg);
            pythonium_call(pythonium_get_attribute(out, "append"), pythonium_get_attribute(r, "jsobject"));
        }
    } catch (x) { if (!pythonium_is_exception(x, StopIteration)) { throw x; }}
    pythonium_call(pythonium_get_attribute(pythonium_get_attribute(console, "log"), "apply"), console, pythonium_get_attribute(out, "jsobject"));
};
var map = function(func, objects) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var out;
    /* BEGIN function */
    out = pythonium_call(list);
    try {
        var __next__ = pythonium_get_attribute(iter(objects), "__next__");
        while(true) {
            var obj = pythonium_call(__next__);
            pythonium_call(pythonium_get_attribute(out, "append"), pythonium_call(func, obj));
        }
    } catch (x) { if (!pythonium_is_exception(x, StopIteration)) { throw x; }}
    return out;
};
/* class definition Generator */
var __init__ = function(self, generator) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "generator", generator);
};
var next = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    try {
        return pythonium_call(pythonium_get_attribute(pythonium_get_attribute(self, "generator"), "next"));
    }
    catch (__exception__) {
        if (pythonium_is_true((pythonium_get_attribute(pythonium_call(pythonium_get_attribute(pythonium_get_attribute(pythonium_create_dict(), "toString"), "call"), __exception__), "__eq__")(pythonium_call(str, "[object StopIteration]"))))) {
            throw StopIteration;
        }
        else {
            throw pythonium_call(Exception, __exception__);
        }
    }
};
var Generator = pythonium_create_class("Generator", [__object], {
    __init__: __init__,
    next: next,
});
/* class definition _True */
var __init__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "jsobject", true);
};
var __and__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true(other === self)) {
        return __TRUE;
    }
    return __FALSE;
};
var __or__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return __TRUE;
};
var __is__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true(other === self)) {
        return __TRUE;
    }
    return __FALSE;
};
var __neg__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return __FALSE;
};
var _True = pythonium_create_class("_True", [__object], {
    __init__: __init__,
    __and__: __and__,
    __or__: __or__,
    __is__: __is__,
    __neg__: __neg__,
});
/* class definition _False */
var __init__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "jsobject", false);
};
var __and__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return __FALSE;
};
var __or__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true(other === True)) {
        return __TRUE;
    }
    return __FALSE;
};
var __is__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true(other === self)) {
        return __TRUE;
    }
    return __FALSE;
};
var __neg__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return __TRUE;
};
var _False = pythonium_create_class("_False", [__object], {
    __init__: __init__,
    __and__: __and__,
    __or__: __or__,
    __is__: __is__,
    __neg__: __neg__,
});
__TRUE = pythonium_call(_True);
__FALSE = pythonium_call(_False);
/* class definition StopIteration */
/* pass */
var StopIteration = pythonium_create_class("StopIteration", [__object], {
});
var iter = function(obj) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call(pythonium_get_attribute(obj, "__iter__"));
};
var next = function(obj) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call(pythonium_get_attribute(obj, "__next__"));
};
var len = function(obj) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call(pythonium_get_attribute(obj, "__len__"));
};
/* class definition ListIterator */
var __init__ = function(self, obj) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "list", obj);
    pythonium_set_attribute(self, "index", pythonium_call(int, 0));
    pythonium_set_attribute(self, "length", pythonium_call(len, obj));
};
var __next__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true((pythonium_get_attribute(pythonium_get_attribute(self, "index"), "__eq__")(pythonium_get_attribute(self, "length"))))) {
        throw StopIteration;
    }
    pythonium_set_attribute(self, "index", (pythonium_call(pythonium_get_attribute(pythonium_get_attribute(self, "index"), "__add__"), pythonium_call(int, 1))));
    return pythonium_call(pythonium_get_attribute(pythonium_get_attribute(self, "list"), '__getitem__'), (pythonium_call(pythonium_get_attribute(pythonium_get_attribute(self, "index"), "__sub__"), pythonium_call(int, 1))));
};
var ListIterator = pythonium_create_class("ListIterator", [__object], {
    __init__: __init__,
    __next__: __next__,
});
/* class definition list */
var __init__ = function(self, jsobject) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    if (__args[__args.length - 2] === __ARGUMENTS_PADDING__) {
        var __kwargs = __args[__args.length - 1];
        var varkwargs_start = __args.length - 2;
    } else {
        var __kwargs = {};
        var varkwargs_start = undefined;
    }
    if (varkwargs_start !== undefined && 1 > varkwargs_start) {
        jsobject = __kwargs.jsobject || __NONE;
    } else {
        jsobject = jsobject || __kwargs.jsobject || __NONE;
    }
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true(jsobject)) {
        pythonium_set_attribute(self, "jsobject", jsobject);
    }
    else {
        pythonium_set_attribute(self, "jsobject", []);
    }
};
var __repr__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var s;
    /* BEGIN function */
    s = (pythonium_call(pythonium_get_attribute((pythonium_call(pythonium_get_attribute(pythonium_call(str, "["), "__add__"), pythonium_call(pythonium_get_attribute(pythonium_call(str, ", "), "join"), self))), "__add__"), pythonium_call(str, "]")));
    return s;
};
var append = function(self, item) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var jsobject;
    /* BEGIN function */
    jsobject = pythonium_get_attribute(self, "jsobject");
    jsobject.push(item);
};
var insert = function(self, index, item) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_call(pythonium_get_attribute(pythonium_get_attribute(self, "jsobject"), "splice"), index, pythonium_call(int, 0), item);
};
var __setitem__ = function(self, index, value) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var jsobject;
    /* BEGIN function */
    jsobject = pythonium_get_attribute(self, "jsobject");
    index = pythonium_get_attribute(index, "jsobject");
    jsobject[index] = value;
};
var __getitem__ = function(self, s) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var index,jsobject;
    /* BEGIN function */
    jsobject = pythonium_get_attribute(self, "jsobject");
    index = pythonium_get_attribute(s, "jsobject");
    return jsobject[index];
};
var __len__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var jsobject,length;
    /* BEGIN function */
    jsobject = pythonium_get_attribute(self, "jsobject");
    length = jsobject.length;
    return pythonium_call(int, length);
};
var __iter__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call(ListIterator, self);
};
var list = pythonium_create_class("list", [__object], {
    __init__: __init__,
    __repr__: __repr__,
    append: append,
    insert: insert,
    __setitem__: __setitem__,
    __getitem__: __getitem__,
    __len__: __len__,
    __iter__: __iter__,
});
/* class definition float */
var __init__ = function(self, jsobject) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "jsobject", jsobject);
};
var __repr__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return self;
};
var __div__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    return pythonium_call(float, a / b);
};
var __sub__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    return pythonium_call(float, a - b);
};
var __eq__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a == b)) {
        return __TRUE;
    }
    return __FALSE;
};
var float = pythonium_create_class("float", [__object], {
    __init__: __init__,
    __repr__: __repr__,
    __div__: __div__,
    __sub__: __sub__,
    __eq__: __eq__,
});
/* class definition _None */
var __and__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true((pythonium_get_attribute(other, "__is__")(__TRUE)))) {
        return __TRUE;
    }
    return __FALSE;
};
var __or__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true((pythonium_get_attribute(other, "__is__")(__TRUE)))) {
        return __TRUE;
    }
    return __FALSE;
};
var __is__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    if (pythonium_is_true(other === self)) {
        return __TRUE;
    }
    return __FALSE;
};
var __neg__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return __TRUE;
};
var _None = pythonium_create_class("_None", [__object], {
    __and__: __and__,
    __or__: __or__,
    __is__: __is__,
    __neg__: __neg__,
});
__NONE = pythonium_call(_None);
/* class definition iterator */
var __init__ = function(self, list) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    /* pass */
};
var iterator = pythonium_create_class("iterator", [__object], {
    __init__: __init__,
});
/* class definition slice */
var __init__ = function(self, start, step, end) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "start", start);
    pythonium_set_attribute(self, "step", step);
    pythonium_set_attribute(self, "end", end);
};
var slice = pythonium_create_class("slice", [__object], {
    __init__: __init__,
});
/* class definition Exception */
var __init__ = function(self, message) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "message", message);
};
var Exception = pythonium_create_class("Exception", [__object], {
    __init__: __init__,
});
/* class definition TypeError */
/* pass */
var TypeError = pythonium_create_class("TypeError", [Exception], {
});
/* class definition AttributeError */
/* pass */
var AttributeError = pythonium_create_class("AttributeError", [Exception], {
});
/* class definition int */
var __init__ = function(self, jsobject) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "jsobject", jsobject);
};
var __repr__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return self;
};
var __add__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    return pythonium_call(int, a + b);
};
var __sub__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    return pythonium_call(int, a - b);
};
var __lt__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a < b)) {
        return __TRUE;
    }
    return __FALSE;
};
var __lte__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a <= b)) {
        return __TRUE;
    }
    return __FALSE;
};
var __mul__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var c,b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    c = a * b;
    return pythonium_call(int, c);
};
var __or__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var c,b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    c = a || b;
    return pythonium_call(int, c);
};
var __eq__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a == b)) {
        return __TRUE;
    }
    return __FALSE;
};
var __neg__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var jsobject;
    /* BEGIN function */
    jsobject = pythonium_get_attribute(self, "jsobject");
    return pythonium_call(int, -jsobject);
};
var __div__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    return pythonium_call(int, a / b);
};
var int = pythonium_create_class("int", [__object], {
    __init__: __init__,
    __repr__: __repr__,
    __add__: __add__,
    __sub__: __sub__,
    __lt__: __lt__,
    __lte__: __lte__,
    __mul__: __mul__,
    __or__: __or__,
    __eq__: __eq__,
    __neg__: __neg__,
    __div__: __div__,
});
/* class definition dict */
var __init__ = function(self, jsobject) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "jsobject", jsobject);
};
var __repr__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var out,value_repr,key_repr;
    /* BEGIN function */
    out = pythonium_call(list);
    try {
        var __next__ = pythonium_get_attribute(iter(pythonium_call(pythonium_get_attribute(self, "keys"))), "__next__");
        while(true) {
            var key = pythonium_call(__next__);
            key_repr = pythonium_call(repr, key);
            value_repr = pythonium_call(repr, pythonium_call(pythonium_get_attribute(self, "get"), key));
            pythonium_call(pythonium_get_attribute(out, "append"), (pythonium_call(pythonium_get_attribute((pythonium_call(pythonium_get_attribute(key_repr, "__add__"), pythonium_call(str, ": "))), "__add__"), value_repr)));
        }
    } catch (x) { if (!pythonium_is_exception(x, StopIteration)) { throw x; }}
    return (pythonium_call(pythonium_get_attribute((pythonium_call(pythonium_get_attribute(pythonium_call(str, "{"), "__add__"), pythonium_call(pythonium_get_attribute(pythonium_call(str, ", "), "join"), out))), "__add__"), pythonium_call(str, "}")));
};
var get = function(self, key, d) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    if (__args[__args.length - 2] === __ARGUMENTS_PADDING__) {
        var __kwargs = __args[__args.length - 1];
        var varkwargs_start = __args.length - 2;
    } else {
        var __kwargs = {};
        var varkwargs_start = undefined;
    }
    if (varkwargs_start !== undefined && 2 > varkwargs_start) {
        d = __kwargs.d || __NONE;
    } else {
        d = d || __kwargs.d || __NONE;
    }
    /* END unpacking arguments */
    var jsobject,attr;
    /* BEGIN function */
    jsobject = pythonium_get_attribute(self, "jsobject");
    key = pythonium_get_attribute(key, "jsobject");
    attr = jsobject[key];
    if (pythonium_is_true((pythonium_get_attribute(__NONE, "__isnot__")(attr)))) {
        return attr;
    }
    else {
        return d;
    }
};
var __setitem__ = function(self, key, value) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_call(pythonium_get_attribute(pythonium_get_attribute(self, "jsobject"), "__setitem__"), key, value);
};
var keys = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call(map, str, pythonium_call(list, pythonium_call(pythonium_get_attribute(Object, "keys"), pythonium_get_attribute(self, "jsobject"))));
};
var items = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var out;
    /* BEGIN function */
    out = pythonium_call(list);
    try {
        var __next__ = pythonium_get_attribute(iter(pythonium_call(pythonium_get_attribute(self, "keys"))), "__next__");
        while(true) {
            var key = pythonium_call(__next__);
            pythonium_call(pythonium_get_attribute(out, "append"), pythonium_call(list, [key, pythonium_call(pythonium_get_attribute(self, "get"), key)]));
        }
    } catch (x) { if (!pythonium_is_exception(x, StopIteration)) { throw x; }}
    return out;
};
var dict = pythonium_create_class("dict", [__object], {
    __init__: __init__,
    __repr__: __repr__,
    get: get,
    __setitem__: __setitem__,
    keys: keys,
    items: items,
});
/* class definition str */
var __init__ = function(self, jsobject) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_set_attribute(self, "jsobject", jsobject);
};
var __repr__ = function(self) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return self;
};
var join = function(self, objects) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var out,obj,index,L;
    /* BEGIN function */
    L = pythonium_call(len, objects);
    if (pythonium_is_true(pythonium_call(pythonium_get_attribute(L, "__neg__")))) {
        return pythonium_call(str, "");
    }
    out = pythonium_call(pythonium_get_attribute(objects, '__getitem__'), pythonium_call(int, 0));
    index = pythonium_call(int, 1);
    while(pythonium_is_true((pythonium_get_attribute(index, "__lt__")(L)))) {
        obj = pythonium_call(pythonium_get_attribute(objects, '__getitem__'), index);
        out = (pythonium_call(pythonium_get_attribute((pythonium_call(pythonium_get_attribute(out, "__add__"), self)), "__add__"), obj));
        index = pythonium_call(pythonium_get_attribute(index, "__add__"), pythonium_call(int, 1));
    }
    return out;
};
var __add__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    return pythonium_call(str, a + b);
};
var __lte__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a <= b)) {
        return __TRUE;
    }
    return __FALSE;
};
var __gte__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a >= b)) {
        return __TRUE;
    }
    return __FALSE;
};
var __gt__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a > b)) {
        return __TRUE;
    }
    return __FALSE;
};
var __eq__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var b,a;
    /* BEGIN function */
    a = pythonium_get_attribute(self, "jsobject");
    b = pythonium_get_attribute(other, "jsobject");
    if (pythonium_is_true(a == b)) {
        return __TRUE;
    }
    return __FALSE;
};
var __getitem__ = function(self, index) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    var c,jsobject;
    /* BEGIN function */
    jsobject = pythonium_get_attribute(self, "jsobject");
    index = pythonium_get_attribute(index, "jsobject");
    c = jsobject[index];
    return pythonium_call(str, c);
};
var __neq__ = function(self, other) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call(pythonium_get_attribute(pythonium_call(pythonium_get_attribute(self, "__eq__"), other), "__neg__"));
};
var str = pythonium_create_class("str", [__object], {
    __init__: __init__,
    __repr__: __repr__,
    join: join,
    __add__: __add__,
    __lte__: __lte__,
    __gte__: __gte__,
    __gt__: __gt__,
    __eq__: __eq__,
    __getitem__: __getitem__,
    __neq__: __neq__,
});
var print = function() {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    var args = __args.splice(0);
    args = pythonium_call(list, args);
    /* END unpacking arguments */
    var out,r;
    /* BEGIN function */
    out = pythonium_call(list);
    try {
        var __next__ = pythonium_get_attribute(iter(args), "__next__");
        while(true) {
            var arg = pythonium_call(__next__);
            r = pythonium_call(repr, arg);
            pythonium_call(pythonium_get_attribute(out, "append"), pythonium_get_attribute(r, "jsobject"));
        }
    } catch (x) { if (!pythonium_is_exception(x, StopIteration)) { throw x; }}
    pythonium_call(pythonium_get_attribute(pythonium_get_attribute(console, "log"), "apply"), console, pythonium_get_attribute(out, "jsobject"));
};
var func = function(a, b, c, d, e) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    if (__args[__args.length - 2] === __ARGUMENTS_PADDING__) {
        var __kwargs = __args[__args.length - 1];
        var varkwargs_start = __args.length - 2;
    } else {
        var __kwargs = {};
        var varkwargs_start = undefined;
    }
    if (varkwargs_start !== undefined && 4 > varkwargs_start) {
        e = __kwargs.e || pythonium_call(int, 5);
    } else {
        e = e || __kwargs.e || pythonium_call(int, 5);
    }
    if (varkwargs_start !== undefined && 5 > varkwargs_start) {
        d = __kwargs.d || pythonium_call(int, 4);
    } else {
        d = d || __kwargs.d || pythonium_call(int, 4);
    }
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_call(print, pythonium_call(str, "results"));
    pythonium_call(print, a, b, c, d, e);
};
pythonium_call(func, pythonium_call(int, 1), pythonium_call(int, 2), pythonium_call(int, 3), pythonium_call(int, 44), pythonium_call(int, 55));
