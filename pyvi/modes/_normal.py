from functools import wraps
from string import digits

from pyvi.mode import Mode
from pyvi.modes import insert


def keypress(mode, editor, key):
    if key == "esc":
        return
    elif key in digits:
        editor.count = (editor.count or 0) * 10 + int(key)
    else:
        mode.dispatch(editor, [key])


normal = Mode(name="Normal", keypress=keypress)


@normal.handles("i")
def i(editor):
    editor.mode = insert
