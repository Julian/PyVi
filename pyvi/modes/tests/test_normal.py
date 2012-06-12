from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import insert, normal


class TestInsertMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor())

    def keypress(self, key):
        normal.keypress(self.editor, key)

    def test_i(self):
        self.keypress("i")
        self.assertEqual(self.editor.mode, insert)
