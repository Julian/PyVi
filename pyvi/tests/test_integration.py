from unittest import TestCase

from pyvi import window


class TestBufferWindowTabInteraction(TestCase):
    def setUp(self):
        self.buffer = window.Buffer()
        self.window = window.Window(self.buffer)
        self.tab = window.Tab(self.window)

    def test_initial_cursor_is_0_0(self):
        self.assertEqual(self.window.cursor, (0, 0))

    def test_single_window_insert(self):
        self.window.insert(u"foo")
        self.window.insert(u"", u"bar", u"quux")
        self.assertEqual(list(self.buffer), [u"foo", u"bar", u"quux"])
        self.assertEqual(self.window.cursor, (2, 4))
