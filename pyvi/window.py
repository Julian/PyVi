import collections
import itertools


class Buffer(object):
    def __init__(self, iterable=""):
        self._iter = iter(iterable)
        self._lines = [collections.deque()]
        self.has_unread_lines = True

    def __getitem__(self, i):
        if isinstance(i, slice):
            self._read_further(how_many=i.stop - self.lines_read)
            lines = itertools.chain.from_iterable(self._lines)
            return list(itertools.islice(lines, i.start, i.stop, i.step))
        else:
            self._read_further(how_many=i - self.lines_read + 1)

        partition, i = self._container_for(i)
        return partition[i]


    def __setitem__(self, i, line):
        if isinstance(i, slice):
            err = "%s object does not support slice assignment."
            raise TypeError(err % self.__class__.__name__)

        self._read_further(how_many=i - self.lines_read + 1)
        partition, i = self._container_for(i)
        partition[i] = line

    def __iter__(self):
        for line in itertools.chain.from_iterable(self._lines):
            yield line
        while self.has_unread_lines:
            self._read_further(how_many=1)
            yield self[-1]

    def __len__(self):
        self._read_further()
        return self.lines_read

    @property
    def lines_read(self):
        return sum(len(partition) for partition in self._lines)

    def _container_for(self, i):
        for partition in self._lines:
            current_len = len(partition)
            if i < current_len:
                return partition, i
            i -= current_len


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

    def append(self, line):
        self._lines[-1].append(line)


class Window(object):
    def __init__(self, buffer):
        self.buffer = buffer
        self._cursor_above = buffer
        self.cursor_column = 0

    @property
    def cursor_row(self):
        return 0


class Tab(object):
    def __init__(self, windows):
        self.windows = windows
