from unittest import TestCase

from pyvi import editor


class TestEditor(TestCase):
    def setUp(self):
        self.editor = editor.Editor(config=mock.Mock(), tabs=[mock.Mock()])
