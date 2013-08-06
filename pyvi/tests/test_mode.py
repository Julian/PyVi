from unittest import TestCase
import mock

from pyvi import mode


class TestMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock()
        self.mode = mode.Mode(editor=self.editor)

    def test_map_new(self):
        a = mock.Mock()
        self.mode.map("a", a)
        self.mode.keypress("a")
        a.assert_called_once_with(self.editor)

    def test_keypress_nonexistant(self):
        b = mock.Mock()
        self.mode.map("b", b)

        self.mode.keypress("a")
        self.assertFalse(b.called)

        self.mode.keypress("b")
        self.assertTrue(b.called)

    def test_map_multiple(self):
        ab = mock.Mock()
        self.mode.map("ab", ab)
        self.mode.keypress("a")
        self.assertFalse(ab.called)

        self.mode.keypress("b")
        ab.assert_called_once_with(self.editor)

    def test_map_multiple_clears_pending_keys(self):
        a, b, ab = mock.Mock(), mock.Mock(), mock.Mock()
        self.mode.map("b", b)
        self.mode.map("ab", ab)

        self.mode.keypress("a")
        self.mode.keypress("b")
        self.assertFalse(a.called)
        self.assertFalse(b.called)
        ab.assert_called_once_with(self.editor)

        self.mode.keypress("b")
        self.assertFalse(a.called)
        b.assert_called_once_with(self.editor)
        self.assertEqual(ab.call_count, 1)
