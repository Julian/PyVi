from pyvi import events, window
from pyvi.modes.normal import Normal


class Editor(object):

    active_tab = None
    next_keyhandler = None

    def __init__(self, tabs=None, config=None, mode=None, Normal=Normal):
        if mode is None:
            mode = Normal(self)

        self.Normal = Normal
        self.events = events.EventHandler()
        self.config = config
        self.count = None
        self.mode = mode

        if tabs is None:
            tabs = self.tabs = [window.Tab(self)]
        else:
            tabs = self.tabs = list(tabs)

        if tabs:
            self.active_tab = tabs[0]

    @property
    def active_window(self):
        return self.active_tab.active_window

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        self.next_keyhandler = mode.keypress

    def keypress(self, key):
        handle, self.next_keyhandler = self.next_keyhandler, self.mode.keypress
        handle(key)
