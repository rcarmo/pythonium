def jQuery(selector):
    return __DOLLAR__(jstype(selector))

input = jQuery('[type="text"]')
button = jQuery('[type="submit"]')
todos = jQuery('#todos')


def add_todo(text):
    li = '<li>' + text + '</li>'
    li = jstype(li)
    todos.append(li)


def on_click(event):
    # event is JavaScript Event
    text = str(input.val())  # convert the JavaScript string to a Python string
    if len(text):
        add_todo(text)


button.click(on_click)
