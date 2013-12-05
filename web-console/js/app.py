editors = {}
for lang in ['css', 'html', 'python']:
    editor = ace.edit(lang + "-editor")
    editors[lang] = editor
    editor.setTheme("ace/theme/monokai")
    editor.getSession().setMode("ace/mode/" + lang)

def compile():
    jQuery.ajax({
        url: '/compile',
        type: 'POST',
        data: {css: editors["css"].getValue(), html: editors["html"].getValue(), python:editors["python"].getValue()},
    })
    jQuery("iframe").src = '/compiled'


jQuery('[value="compile"]').click(compile)
