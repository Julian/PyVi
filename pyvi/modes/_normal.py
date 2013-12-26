from functools import wraps
from string import digits

from pyvi.mode import Mode
from pyvi.modes import insert


def motion(fn):
    @wraps(fn)
    def move(editor):
        cursor = editor.active_window.cursor
        moved_to = fn(editor, count=editor.count or 1)
        # XXX: do this on any executed command
        editor.count = None

        command = editor._command
        if command is not None:
            command(editor, motion=moved_to)
            editor._command = None
        else:
            cursor.coords = moved_to
            cursor.trim()
    return move


def operator(fn):
    @wraps(fn)
    def operate(editor):
        editor._command = fn
    return operate


def keypress(mode, editor, key):
    if key == "esc":
        return
    elif key in digits:
        editor.count = (editor.count or 0) * 10 + int(key)
    else:
        mode.dispatch(editor, [key])


normal = Mode(name="Normal", keypress=keypress)


@normal.handles("d")
@operator
def d(editor, motion):
    buffer = editor.active_window.buffer
    row, column = editor.active_window.cursor
    end_row, end_column = motion

    if row == end_row:
        line = buffer.lines[row]
        buffer.lines[row] = line[:column] + line[end_column:]
    else:
        buffer.lines[row] = buffer.lines[row][:column]
        buffer.lines[row + 1:end_row] = []
        buffer.lines[end_row] = buffer.lines[row][end_column:]


@normal.handles("h")
@motion
def h(editor, count):
    row, column = editor.active_window.cursor
    return row, column - count


@normal.handles("i")
def i(editor):
    editor.mode = insert


@normal.handles("j")
@motion
def j(editor, count):
    row, column = editor.active_window.cursor
    return row + count, column


@normal.handles("k")
@motion
def k(editor, count):
    row, column = editor.active_window.cursor
    return row - count, column


@normal.handles("l")
@motion
def l(editor, count):
    row, column = editor.active_window.cursor
    return row, column + count
