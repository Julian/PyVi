def map(keymap):
    def _map(key):
        def mapped(fn):
            keymap[key] = fn
            return fn
        return mapped
    return _map
