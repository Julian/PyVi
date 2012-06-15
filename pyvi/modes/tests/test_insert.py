from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import insert
from pyvi.tests.util import MockCursor


class TestInsertMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor())
        self.cursor = self.editor.active_window.cursor = MockCursor(
            row=0, column=1
        )

    def test_esc(self):
        self.assertEqual(self.cursor.coords, (0, 1))
        insert.keypress(self.editor, u"esc")
        self.assertEqual(self.editor.mode, self.editor.normal_mode)
        self.assertEqual(self.cursor.coords, (0, 0))

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
