from pyvi import events
from pyvi.modes import normal


class Editor(object):

    active_tab = None

    def __init__(self, tabs=(), config=None, mode=None, normal_mode=normal):
        if mode is None:
            mode = normal_mode

        self.events = events.EventHandler()
        self.config = config
        self.mode = mode
        self.normal_mode = normal_mode
        self.tabs = []

        for tab in tabs:
            self.add_tab(tab)

        if self.tabs:
            self.active_tab = self.tabs[0]

    @property
    def active_window(self):
        return self.active_tab.active_window

    def add_tab(self, tab):
        tab.editor = self
        self.tabs.append(tab)

    def keypress(self, key):
        if key == "esc":
            self.mode = self.normal_mode
        else:
            self.mode.keypress(self, key)
