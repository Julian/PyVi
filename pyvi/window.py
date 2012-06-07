import collections
import itertools


class Buffer(object):
    def __init__(self, iterable=(u"",)):
        self._iter = iter(iterable)
        self._lines = []
        self.has_unread_lines = True

        self.cursors = {}

    def __getitem__(self, i):
        if isinstance(i, slice):
            self._read_further(how_many=i.stop - self.lines_read)
        else:
            self._read_further(how_many=i - self.lines_read + 1)
        return self._lines[i]


    def __setitem__(self, i, value):
        if isinstance(i, slice):
            self._read_further(how_many=i.stop - self.lines_read)
        else:
            self._read_further(how_many=i - self.lines_read + 1)
        self._lines[i] = value

    def __iter__(self):
        for line in self._lines:
            yield line
        while self.has_unread_lines:
            self._read_further(how_many=1)
            yield self[-1]

    def __len__(self):
        self._read_further()
        return self.lines_read

    @property
    def lines_read(self):
        return len(self._lines)


    def _read_further(self, how_many=None):
        if not self.has_unread_lines:
            return

        if how_many is not None:
            lines = (next(self._iter) for _ in xrange(how_many))
        else:
            lines = self._iter
            self.has_unread_lines = False

        for line in lines:
            self.append(line)

    def create_cursor(self, owner, at=(0, 0)):
        self.cursors[owner] = at

    def append(self, line):
        self._lines.append(line)

    def insert(self, cursor_owner, first_line, *lines):
        row, column = self.cursors[cursor_owner]
        left, right = self[row][:column], self[row][column:]
        last_line = lines[-1] if lines else first_line
        added = len(lines)

        self[row] = left + first_line
        self[row + 1: row + 1] = lines
        new_row, new_column = row + added, len(last_line)
        self[new_row] += right
        self.cursors[cursor_owner] = new_row, new_column

        for owner, (other_row, other_column) in self.cursors.iteritems():
            if owner != cursor_owner and other_row > row:
                self.cursors[owner] = (other_row + added, other_column)


class Window(object):
    def __init__(self, buffer, cursor=(0, 0)):
        self.buffer = buffer
        buffer.create_cursor(self)
        self.cursor = cursor

    @property
    def cursor(self):
        return self.buffer.cursors[self]

    @cursor.setter
    def cursor(self, new_position):
        self.buffer.cursors[self] = new_position

    def insert(self, *lines):
        self.buffer.insert(self, *lines)


class Tab(object):
    def __init__(self, *windows):
        self.windows = list(windows)
