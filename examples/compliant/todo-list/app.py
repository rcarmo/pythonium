def jQuery(selector):
    return __DOLLAR__(jstype(selector))

input = jQuery('[type="text"]')
button = jQuery('[type="submit"]')

def on_click(event):
    print('Héy')

button.click(on_click)
