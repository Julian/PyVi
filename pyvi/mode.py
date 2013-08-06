from collections import MutableMapping


class Mode(object):
    def __init__(self, editor, map=()):
        self._editor = editor
        self._map = _Map()

        for key, handler in dict(map).iteritems():
            self.map(key, handler)

    def map(self, key, to):
        self._map.add(key, to)

    def keypress(self, keys):
        handler = self._map.handler_for(keys)
        if handler is not None:
            handler(self._editor)


class _Map(object):
    def __init__(self):
        self.contents = None, {}
        self.pending = ""

    def add(self, keys, handler):
        _, mapping = self.contents
        for key in keys[:-1]:
            _, mapping = mapping.setdefault(key, (None, {}))
        mapping[keys[-1]] = handler, {}

    def handler_for(self, keys):
        handler, mapping = self.contents
        for key in self.pending + keys:
            if key not in mapping:
                handler, self.pending = None, ""
                return

            handler, mapping = mapping[key]

        if mapping:
            self.pending += keys
            return

        self.pending = ""
        return handler
