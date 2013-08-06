class StubCursor(object):
    column = 0
    row = 0

    def __iter__(self):
        return iter([self.row, self.column])

    @property
    def coords(self):
        return self.row, self.column

    @coords.setter
    def coords(self, coords):
        self.row, self.column = coords
