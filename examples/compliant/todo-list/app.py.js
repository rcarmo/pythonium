var jQuery = function(selector) {
    /* BEGIN arguments unpacking */
    /* END arguments unpacking */
    /* BEGIN function */
    var call_arguments0 = [jstype, selector];
    var call_arguments1 = [$, pythonium_call.apply(undefined, call_arguments0)];
    return pythonium_call.apply(undefined, call_arguments1);
    return __NONE;
};

var call_arguments2 = [jQuery, pythonium_call(str, '[type="text"]')];
input = pythonium_call.apply(undefined, call_arguments2);
var call_arguments3 = [jQuery, pythonium_call(str, '[type="submit"]')];
button = pythonium_call.apply(undefined, call_arguments3);
var call_arguments4 = [jQuery, pythonium_call(str, "#todos")];
todos = pythonium_call.apply(undefined, call_arguments4);
var add_todo = function(text) {
    /* BEGIN arguments unpacking */
    /* END arguments unpacking */
    var li;
    /* BEGIN function */
    li = (pythonium_call(pythonium_get_attribute((pythonium_call(pythonium_get_attribute(pythonium_call(str, "<li>"), "__add__"), text)), "__add__"), pythonium_call(str, "</li>")));
    var call_arguments5 = [jstype, li];
    li = pythonium_call.apply(undefined, call_arguments5);
    var call_arguments6 = [pythonium_get_attribute(todos, "append"), li];
    pythonium_call.apply(undefined, call_arguments6);
};

var on_click = function(event) {
    /* BEGIN arguments unpacking */
    /* END arguments unpacking */
    var text;
    /* BEGIN function */
    var call_arguments7 = [pythonium_get_attribute(input, "val")];
    var call_arguments8 = [str, pythonium_call.apply(undefined, call_arguments7)];
    text = pythonium_call.apply(undefined, call_arguments8);
    var call_arguments9 = [len, text];
    if (pythonium_is_true(pythonium_call.apply(undefined, call_arguments9))) {
        var call_arguments10 = [add_todo, text];
        pythonium_call.apply(undefined, call_arguments10);
    }
};

var call_arguments11 = [pythonium_get_attribute(button, "click"), on_click];
pythonium_call.apply(undefined, call_arguments11);
