class Mode(object):
    def __init__(self, name, keypress=None):
        if keypress is None:
            keypress = lambda _, editor, key: self.dispatch(editor, [key])

        self.name = name
        self._keypress = keypress
        self._map = _Map()

    def __repr__(self):
        return "<{self.__class__.__name__}: {self.name}>".format(self=self)

    def handles(self, keys):
        """
        Add the decorated callable as a handler for the given key (sequence).

        """

        def _handles(fn):
            self._map.add(keys, fn)
            return fn
        return _handles

    def map(self, key, to):
        self._map.add(key, to)

    def dispatch(self, editor, keys):
        """
        Dispatch the given keys to the underlying mode map.

        """

        handler = self._map.handler_for(keys)
        if handler is not None:
            handler(editor)

    def keypress(self, editor, keys):
        for key in keys:
            self._keypress(self, editor, key)


class _Map(object):
    def __init__(self):
        self._contents = None, {}
        self._pending_keys = []

    def add(self, keys, handler):
        """
        Add a handler for the given keys.

        """

        _, mapping = self._contents
        for key in keys[:-1]:
            _, mapping = mapping.setdefault(key, (None, {}))
        mapping[keys[-1]] = handler, {}

    def handler_for(self, keys):
        """
        Retrieve the handler for the given keys if complete.

        Otherwise, stores the partial key input for a successive call.

        """

        handler, mapping = self._contents
        for key in self._pending_keys + keys:
            if key not in mapping:
                return self.clear()
            handler, mapping = mapping[key]

        if mapping:
            self._pending_keys += keys
            return

        self.clear()
        return handler

    def clear(self):
        """
        Clear any partial input.

        """

        self._pending_keys = []
