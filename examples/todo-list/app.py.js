var jQuery = function(selector) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    return pythonium_call($, pythonium_call(jstype, selector));
};
input = pythonium_call(jQuery, pythonium_call(str, '[type="text"]'));
button = pythonium_call(jQuery, pythonium_call(str, '[type="submit"]'));
var on_click = function(event) {
    /* BEGIN unpacking arguments */
    var __args = Array.prototype.slice.call(arguments);
    /* END unpacking arguments */
    /* BEGIN function */
    pythonium_call(print, pythonium_call(str, "Héy"));
};
pythonium_call(pythonium_get_attribute(button, "click"), on_click);
