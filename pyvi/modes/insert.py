from pyvi import events
from pyvi.mode import Mode


class Insert(Mode):

    name = "insert"

    def keypress(self, key):
        if key == "esc":
            self.editor.mode = self.editor.Normal(self.editor)
            self.editor.active_window.cursor.column -= 1
        else:
            insert(self.editor, key)


def insert(editor, key):
    editor.events.trigger(event=events.INSERT_CHAR_PRE, char=key)

    if key == u"tab":
        key = u"\t"

    if key == u"enter":
        editor.active_window.insert(u"", u"")
    else:
        editor.active_window.insert(key)

    editor.events.trigger(event=events.INSERT_CHAR, char=key)
