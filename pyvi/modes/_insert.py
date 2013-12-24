from pyvi.mode import Mode


def keypress(mode, editor, key):
    if key == "esc":
        editor.mode = editor.normal
        editor.active_window.cursor.column -= 1
    elif key == "backspace":
        editor.active_window.backspace()
    else:
        # editor.events.trigger(event=events.INSERT_CHAR_PRE, char=key)

        if key == u"tab":
            key = u"\t"

        if key == u"enter":
            editor.active_window.insert(u"", u"")
        else:
            editor.active_window.insert(key)

        # editor.events.trigger(event=events.INSERT_CHAR, char=key)


insert = Mode(name="Insert", keypress=keypress)
