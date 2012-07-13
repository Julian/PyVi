import itertools

from pyvi import events


class Buffer(object):
    def __init__(self, iterable=(u"",)):
        self._iter = iter(iterable)
        self._lines = []
        self.done_reading = False
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
        while True:
            self._read_further(how_many=1)

            if not self.done_reading:
                yield self[-1]
            else:
                return

    def __len__(self):
        self._read_further()
        return self.lines_read

    @property
    def lines_read(self):
        return len(self._lines)


    def _read_further(self, how_many=None):
        if self.done_reading:
            return

        if how_many is not None:
            for _ in xrange(how_many):
                try:
                    self.append(next(self._iter))
                except StopIteration:
                    self.done_reading = True
                    return
        else:
            self._lines.extend(self._iter)
            self.done_reading = True

    def append(self, line):
        self._lines.append(line)

    def chars(self, start=(0, 0), end=None):
        if end is None:
            end = (len(self) - 1, len(self[-1]))

        first_row, first_col = start
        last_row, last_col = end

        # XXX
        if first_row == last_row:
            return self[first_row][first_col:last_col]

        first = self[first_row][first_col:]
        middle = itertools.chain.from_iterable(self[first_row + 1:last_row])
        last = self[last_row][:last_col]

        return itertools.chain(first, middle, last)

    def delete(self, start=(0, 0), end=None):
        if end is None:
            end = (len(self) - 1, len(self[-1]))

        first_row, first_col = start
        last_row, last_col = end

        # XXX
        if first_row == last_row:
            row = self[first_row]
            self[first_row] = row[:first_col] + row[last_col:]
        else:
            self[first_row] = self[first_row][:first_col]
            self[last_row] = self[last_row][last_col:]
            self[first_row + 1:last_row] = []

    def insert(self, window, first_line, *lines):
        row, column = cursor = self.cursors[window]
        left, right = self[row][:column], self[row][column:]
        added = len(lines)

        if lines:
            last_line = lines[-1]
            column = len(last_line)
        else:
            last_line = first_line
            column += len(first_line)

        self[row] = left + first_line
        self[row + 1: row + 1] = lines
        self[row + added] += right

        for other in self.cursors.itervalues():
            if other.row > row:
                other._row += added

        cursor.coords = row + added, column

    def write(self, file):
        file.writelines(line + "\n" for line in self)


class Cursor(object):
    def __init__(self, window, coords=(0, 0)):
        self._row, self._column = coords
        self.trigger = window.editor.events.trigger
        self.window = window
        window.buffer.cursors[window] = self

    def __eq__(self, other):
        return self.coords == other

    def __iter__(self):
        yield self.row
        yield self.column

    def __ne__(self, other):
        return self.coords != other

    def __repr__(self):
        return repr(self.coords)

    def __reversed__(self):
        yield self.column
        yield self.row

    @property
    def coords(self):
        return self._row, self._column

    @coords.setter
    def coords(self, coords):
        self._row, self._column = coords
        self.trigger(event=events.CURSOR_MOVED)

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, column):
        self._column = column
        self.trigger(event=events.CURSOR_MOVED)

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row
        self.trigger(event=events.CURSOR_MOVED)

    def trim(self):
        # XXX: Should this fire an event?
        row, column, buffer = self._row, self._column, self.window.buffer
        self._row = row = max(min(len(buffer) - 1, row), 0)
        self._column = max(min(len(buffer[row]) - 1, column), 0)


class Window(object):
    def __init__(self, editor, buffer=None, cursor=(0, 0)):
        if buffer is None:
            buffer = Buffer()

        self.editor = editor
        self.buffer = buffer
        self.cursor = Cursor(self, coords=cursor)

    def insert(self, *lines):
        self.buffer.insert(self, *lines)

    def chars(self, start=None, *args, **kwargs):
        if start is None:
            start = self.cursor.coords
        return self.buffer.chars(start=start, *args, **kwargs)

    def delete(self, start=None, *args, **kwargs):
        if start is None:
            start = self.cursor.coords
        return self.buffer.delete(start=start, *args, **kwargs)


class Tab(object):

    active_window = None

    def __init__(self, editor, windows=None):
        self.editor = editor

        if windows is None:
            window = self.active_window = Window(editor)
            self.windows = [[window]]
        else:
            self.windows = windows

    def __iter__(self):
        return iter(self.windows)
