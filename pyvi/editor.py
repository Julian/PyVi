from pyvi import events, window
from pyvi.modes.normal import Normal


class Editor(object):

    active_tab = None

    def __init__(self, tabs=None, config=None, mode=None, Normal=Normal):
        if mode is None:
            mode = Normal(self)

        self.Normal = Normal
        self.events = events.EventHandler()
        self.config = config
        self.count = None
        self.mode = mode

        if tabs is None:
            tab = window.Tab(self)
            tabs = [tab]
            self.active_tab = tab

        self.tabs = tabs

    @property
    def active_window(self):
        return self.active_tab.active_window

    def keypress(self, key):
        self.mode.keypress(key)
