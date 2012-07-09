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

    def keypress(self, key):
        cmdline.keypress(self.editor, key)

    def test_esc(self):
        self.keypress("esc")
        self.assertEqual(self.editor.mode, self.editor.normal_mode)

    def test_insert(self):
        self.keypress(u"f")
        self.editor.active_window.insert.assert_called_once_with(u"f")
        self.keypress(u"/")
