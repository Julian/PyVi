from pyvi import events
from pyvi.modes import key


KEYMAP = {}
map_to = key.map(KEYMAP)


def keypress(editor, key):
    if key == "esc":
        editor.mode = editor.normal_mode

    editor.active_window.insert(key)
    editor.events.trigger(event=events.INSERT_CHAR, char=key)
