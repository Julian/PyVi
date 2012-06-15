from functools import wraps
from string import digits

from pyvi.modes import insert


def keypress(editor, key):
    if key == "esc":
        return
    elif key in digits:
        editor.count = (editor.count or 0) * 10 + int(key)
    elif key == "i":
        editor.mode = insert
    else:
        KEYMAP[key](editor)


def motion(fn):
    @wraps(fn)
    def move(editor, *args, **kwargs):
        cursor_position = fn(editor, count=editor.count or 1, *args, **kwargs)
        editor.count = None
        editor.active_window.cursor.coords = cursor_position
    return move


@motion
def h(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row, cursor.column - count


@motion
def j(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row + count, cursor.column


@motion
def k(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row - count, cursor.column


@motion
def l(editor, count):
    cursor = editor.active_window.cursor
    return cursor.row, cursor.column + count


KEYMAP = {
    "h" : h,
    "j" : j,
    "k" : k,
    "l" : l,
}
