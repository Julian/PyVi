from pyvi import events


class Buffer(object):
    def __init__(self, iterable=(u"",)):
        self._iter = iter(iterable)
        self._lines = []
        self.done_reading = False

        self.cursors = events.NoisyContainer(
            {}, event=events.CURSOR_MOVED, key_label="window"
        )

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
        while not self.done_reading:
            self._read_further(how_many=1)
            yield self[-1]

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
            lines = (next(self._iter) for _ in xrange(how_many))
        else:
            lines = self._iter
            self.done_reading = True

        for line in lines:
            self.append(line)

    def create_cursor(self, owner, at=(0, 0)):
        self.cursors[owner] = at

    def append(self, line):
        self._lines.append(line)

    def insert(self, cursor_owner, first_line, *lines):
        row, column = self.cursors[cursor_owner]
        left, right = self[row][:column], self[row][column:]
        added = len(lines)

        if lines:
            last_line = lines[-1]
            new_column = len(last_line)
        else:
            last_line = first_line
            new_column = column + len(first_line)

        self[row] = left + first_line
        self[row + 1: row + 1] = lines
        new_row = row + added
        self[new_row] += right
        self.cursors[cursor_owner] = new_row, new_column

        for owner, (other_row, other_column) in self.cursors.iteritems():
            if owner != cursor_owner and other_row > row:
                self.cursors[owner] = (other_row + added, other_column)


class Window(object):

    editor = None
    events = None

    def __init__(self, buffer=None, cursor=(0, 0)):
        if buffer is None:
            buffer = Buffer()

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

    def trigger(self, **event):
        if self.events is not None:
            self.events.trigger(**event)


class Tab(object):

    active_window = None
    _editor = None
    events = None

    def __init__(self, windows=None):
        if windows is None:
            self.windows = [[Window()]]
        else:
            self.windows = [list(row) for row in windows]

        if self.windows:
            self.active_window = self.windows[0][0]

    def __iter__(self):
        return iter(self.windows)

    @property
    def editor(self):
        return self._editor

    @editor.setter
    def editor(self, editor):
        self._editor = editor
        self.events = editor.events

        for row in self:
            for window in row:
                window.editor = editor
                window.events = editor.events
