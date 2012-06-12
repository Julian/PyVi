from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import insert


class TestInsertMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor)

    def test_inserts_characters(self):
        insert.keypress(self.editor, "f")
        self.editor.active_window.insert.assert_called_once_with("f")
