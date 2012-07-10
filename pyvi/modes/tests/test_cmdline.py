from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import cmdline
from pyvi.tests.util import MockCursor


class TestCmdlineMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor(), count=None)
        self.window = self.editor.active_window
        self.cursor = self.window.cursor = MockCursor(row=1, column=1)
        self.mode = cmdline.Cmdline(self.editor)

    def keypress(self, key):
        self.mode.keypress(key)

    def test_esc(self):
        self.keypress("esc")
        self.assertEqual(self.editor.mode, self.editor.Normal(self.editor))

    def test_insert(self):
        self.keypress(u"f")
        self.editor.active_window.insert.assert_called_once_with(u"f")
        self.keypress(u"/")
