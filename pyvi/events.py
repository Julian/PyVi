import panglery


CURSOR_MOVED = "cursor_moved"


EventHandler = panglery.Pangler


class NoisyContainer(object):
    def __init__(self, contents, trigger=None, key_label=None, **kw):
        self._contents = contents
        self.trigger_fn = trigger
        self.kw = kw
        self.key_label = key_label

        for attr in [
            "iteritems", "items", "itervalues", "values", "iterkeys", "keys"
        ]:
            fn = getattr(contents, attr)
            if fn is not None:
                setattr(self, attr, fn)

    def __getitem__(self, i):
        return self._contents[i]

    def __setitem__(self, i, j):
        self._contents[i] = j
        if self.trigger_fn is None:
            self.trigger_fn = i.trigger
        self.trigger(i, j)

    def __str__(self):
        return str(self._contents)

    def __repr__(self):
        return repr(self._contents)

    def trigger(self, i, j):
        if self.key_label is not None:
            self.kw[self.key_label] = i
        self.trigger_fn(**self.kw)
