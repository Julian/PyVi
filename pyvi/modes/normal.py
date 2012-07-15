from functools import wraps
from string import digits

from pyvi.modes import insert
from pyvi.mode import Mode


def motion(fn):
    @wraps(fn)
    def move(self):
        cursor = self.editor.active_window.cursor
        moved_to = fn(self, count=self.editor.count or 1)
        # XXX: do this on any executed command
        self.editor.count = None

        command = self.editor._command
        if command is not None:
            command(self, motion=moved_to)
            self.editor._command = None
        else:
            cursor.coords = moved_to
            cursor.trim()
    return move


def operator(fn):
    @wraps(fn)
    def operate(self):
        self.editor._command = fn
    return operate


class Normal(Mode):

    name = "normal"

    def keypress(self, key):
        if key == "esc":
            return
        elif key in digits:
            self.editor.count = (self.editor.count or 0) * 10 + int(key)
        else:
            super(Normal, self).keypress(key)

    @operator
    def keypress_d(self, motion):
        buffer = self.editor.active_window.buffer
        row, column = self.editor.active_window.cursor
        end_row, end_column = motion

        if row == end_row:
            line = buffer.lines[row]
            buffer.lines[row] = line[:column] + line[end_column:]
        else:
            buffer.lines[row] = buffer.lines[row][:column]
            buffer.lines[row + 1:end_row] = []
            buffer.lines[end_row] = buffer.lines[row][end_column:]

    @motion
    def keypress_h(self, count):
        row, column = self.editor.active_window.cursor
        return row, column - count

    def keypress_i(self):
        self.editor.mode = insert.Insert(self.editor)

    @motion
    def keypress_j(self, count):
        row, column = self.editor.active_window.cursor
        return row + count, column


    @motion
    def keypress_k(self, count):
        row, column = self.editor.active_window.cursor
        return row - count, column


    @motion
    def keypress_l(self, count):
        row, column = self.editor.active_window.cursor
        return row, column + count
