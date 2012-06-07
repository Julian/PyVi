from unittest import TestCase

from pyvi import window


class TestBufferWindowTabInteraction(TestCase):
    def setUp(self):
        self.buffer = window.Buffer()
        self.window = window.Window(self.buffer)
        self.tab = window.Tab(self.window)

    def test_initial_cursor_is_0_0(self):
        self.assertEqual(self.window.cursor, (0, 0))

    def test_set_cursor(self):
        self.window.cursor = 2, 2
        self.assertEqual(self.window.cursor, (2, 2))

    def test_single_window_insert(self):
        self.window.insert(u"foo")
        self.window.insert(u"", u"bar", u"quux")
        self.assertEqual(list(self.buffer), [u"foo", u"bar", u"quux"])
        self.assertEqual(self.window.cursor, (2, 4))

    def test_multiple_window_insert(self):
        self.buffer.insert(self.window, u"foo", u"bar", u"baz", u"quux", u"")
        another = window.Window(self.buffer, cursor=(2, 3))
        and_another = window.Window(self.buffer, cursor=(0, 0))

        self.window.insert(u"spam")
        another.insert(u"", u"eggs")
        and_another.insert(u"cheese", u"")

        lines = [u"cheese", u"foo", u"bar", u"baz", u"eggs", u"quux", u"spam"]
        self.assertEqual(list(self.buffer), lines)

        self.assertEqual(self.window.cursor, (6, 4))
        self.assertEqual(another.cursor, (4, 4))
        self.assertEqual(and_another.cursor, (1, 0))
