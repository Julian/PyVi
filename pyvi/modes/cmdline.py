from pyvi import events
from pyvi.modes.insert import insert
from pyvi.mode import Mode


class Cmdline(Mode):
    def keypress(self, key):
        if key == "esc":
            # XXX: dismiss window
            super(Cmdline, self).keypress(key)
        else:
            insert(self.editor, key)
