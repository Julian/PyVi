from functools import wraps
from string import digits

from pyvi.modes import key, insert


KEYMAP = {}
map_to = key.map(KEYMAP)


def keypress(editor, key):
    if key == "esc":
        return
    elif key in digits:
        editor.count = (editor.count or 0) * 10 + int(key)
    elif key == "i":
        editor.mode = insert
    else:
        fn = KEYMAP.get(key)

        if fn is not None:
            fn(editor)


def motion(fn):
    @wraps(fn)
    def move(editor, *args, **kwargs):
        cursor = editor.active_window.cursor
        moved_to = fn(editor, count=editor.count or 1, *args, **kwargs)
        editor.count = None
        cursor.coords = moved_to
        cursor.trim()
    return move


@map_to("h")
@motion
def h(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row, cursor.column - count


@map_to("j")
@motion
def j(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row + count, cursor.column


@map_to("k")
@motion
def k(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row - count, cursor.column


@map_to("l")
@motion
def l(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row, cursor.column + count
