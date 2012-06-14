from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import insert


class TestInsertMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor())

    def test_inserts_characters(self):
        insert.keypress(self.editor, u"f")
        self.editor.active_window.insert.assert_called_once_with(u"f")
        insert.keypress(self.editor, u"/")
        self.editor.active_window.insert.assert_called_with(u"/")

    def test_insert_tab(self):
        insert.keypress(self.editor, u"tab")
        self.editor.active_window.insert.assert_called_once_with(u"\t")

    def test_insert_nontext(self):
        insert.keypress(self.editor, u"enter")
        self.editor.active_window.insert.assert_called_once_with(u"", u"")
