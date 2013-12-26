from pyvi import window
from pyvi.modes import normal


class Editor(object):

    _command = None
    active_tab = None

    def __init__(self, tabs=None, config=None, normal=normal):
        self.config = config
        self.mode = self.normal = normal
        self.count = None

        if tabs is None:
            tabs = self.tabs = [window.Tab(self)]
        else:
            tabs = self.tabs = list(tabs)

        if tabs:
            self.active_tab = tabs[0]

    @property
    def active_window(self):
        return self.active_tab.active_window

    def keypress(self, keys):
        return self.mode.keypress(self, keys)
