from functools import wraps
from string import digits

from pyvi.modes import insert
from pyvi.mode import Mode


def motion(fn):
    @wraps(fn)
    def move(self, *args, **kwargs):
        cursor = self.editor.active_window.cursor
        self.editor.count = self.editor.count or 1
        moved_to = fn(self, *args, **kwargs)
        # XXX: do this on any executed command
        self.editor.count = None
        cursor.coords = moved_to
        cursor.trim()
    return move


class Normal(Mode):
    def keypress(self, key):
        if key == "esc":
            return
        elif key in digits:
            self.editor.count = (self.editor.count or 0) * 10 + int(key)
        else:
            super(Normal, self).keypress(key)

    @motion
    def keypress_h(self):
        cursor = self.editor.active_window.cursor
        return cursor.row, cursor.column - self.editor.count

    def keypress_i(self):
        self.editor.mode = insert.Insert(self.editor)

    @motion
    def keypress_j(self):
        cursor = self.editor.active_window.cursor
        return cursor.row + self.editor.count, cursor.column


    @motion
    def keypress_k(self):
        cursor = self.editor.active_window.cursor
        return cursor.row - self.editor.count, cursor.column


    @motion
    def keypress_l(self):
        cursor = self.editor.active_window.cursor
        return cursor.row, cursor.column + self.editor.count
