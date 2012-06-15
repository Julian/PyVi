from pyvi import events


def keypress(editor, key):
    if key == "esc":
        editor.mode = editor.normal_mode
        editor.active_window.cursor.column -= 1
        return

    editor.events.trigger(event=events.INSERT_CHAR_PRE, char=key)

    if key == u"tab":
        key = u"\t"

    if key == "enter":
        editor.active_window.insert(u"", u"")
    else:
        editor.active_window.insert(key)

    editor.events.trigger(event=events.INSERT_CHAR, char=key)
