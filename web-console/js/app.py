editors = {}
for lang in ['css', 'html', 'python']:
    editor = ace.edit(lang + "-editor")
    editors[lang] = editor
    editor.setTheme("ace/theme/monokai")
    editor.getSession().setMode("ace/mode/" + lang)

def reload_iframe():
    document.getElementById("result").contentDocument.location.reload(True)

def compile():
    mode = jQuery("select").val()
    jQuery.ajax({
        url: 'compile',
        type: 'POST',
        data: {css: editors["css"].getValue(), html: editors["html"].getValue(), python:editors["python"].getValue(), mode: mode},
    }).done(reload_iframe)



jQuery('[value="compile"]').click(compile)
