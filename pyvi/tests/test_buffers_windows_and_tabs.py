from unittest import TestCase

import mock

from pyvi import editor, window


class TestBuffer(TestCase):
    def test_empty_buffer_has_one_empty_line(self):
        b = window.Buffer()
        self.assertEqual(len(b), 1)
        self.assertEqual(list(b), [u""])

    def test_get_line_by_index(self):
        lines = [u"foo", u"bar", u"baz"]
        b = window.Buffer(lines)
        self.assertEqual(b[0], lines[0])

    def test_no_such_line_raises_IndexError(self):
        with self.assertRaises(IndexError):
            window.Buffer()[5]

        with self.assertRaises(IndexError):
            window.Buffer()[5] = "bar"

    def test_set_line_by_index(self):
        lines = [u"foo", u"bar", u"baz"]
        b = window.Buffer(lines)

        b[1] = lines[1] = u"quux"
        self.assertEqual(list(b), lines)

    def test_set_slice(self):
        b = window.Buffer()
        b[:3] = lines = [u"foo", u"bar", u"baz"]
        self.assertEqual(list(b), lines)

    def test_seeks_forward_for_unread_lines(self):
        b = window.Buffer((unicode(i) for i in xrange(100)))
        self.assertEqual(b.lines_read, 0)
        self.assertEqual(b[:10], [unicode(i) for i in xrange(10)])

        self.assertEqual(b.lines_read, 10)
        self.assertEqual(b[10], u"10")
        self.assertEqual(b.lines_read, 11)


class TestBufferCursor(TestCase):
    def setUp(self):
        self.lines = [u"foo", u"bar", u"baz"]
        self.buffer = window.Buffer(self.lines)
        self.cursor_owner = mock.Mock()
        self.buffer.create_cursor(self.cursor_owner)

    def test_create_cursor(self):
        self.assertEqual(self.buffer.cursors[self.cursor_owner], (0, 0))
        self.buffer.create_cursor(self.cursor_owner, at=(1, 1))
        self.assertEqual(self.buffer.cursors[self.cursor_owner], (1, 1))

    def test_set_cursor(self):
        self.buffer.cursors[self.cursor_owner] = 2, 2
        self.assertEqual(self.buffer.cursors[self.cursor_owner], (2, 2))

    def test_insert(self):
        self.buffer.insert(self.cursor_owner, u"fo")
        self.assertEqual(self.buffer.cursors[self.cursor_owner], (0, 2))

        self.buffer.insert(self.cursor_owner, u"o")
        self.assertEqual(self.buffer.cursors[self.cursor_owner], (0, 3))

        self.buffer.insert(self.cursor_owner, u"bar", u"baz", u"quux")
        self.assertEqual(self.buffer.cursors[self.cursor_owner], (2, 4))

        self.buffer.insert(self.cursor_owner, u"", u"")
        self.assertEqual(self.buffer.cursors[self.cursor_owner], (3, 0))

        self.assertEqual(
            list(self.buffer), [u"foobar", u"baz", u"quux"] + self.lines,
        )


class TestWindow(TestCase):
    pass


class TestTab(TestCase):
    def setUp(self):
        self.windows = [[mock.Mock(), mock.Mock()], [mock.Mock(), mock.Mock()]]
        self.tab = window.Tab(windows=self.windows)

    def test_active_window(self):
        self.assertEqual(self.tab.active_window, self.windows[0][0])

    def test_forwards_editor_and_events(self):
        self.tab.editor = mock.Mock()

        self.assertEqual(
            {window.editor for row in self.tab for window in row},
            {self.tab.editor}
        )
        self.assertEqual(
            {window.events for row in self.tab for window in row},
            {self.tab.editor.events}
        )

    def test_iter_returns_rows(self):
        first, second = list(self.tab)
        self.assertEqual(first, self.windows[0])
        self.assertEqual(second, self.windows[1])



class TestEditor(TestCase):
    def setUp(self):
        self.editor = editor.Editor(config=mock.Mock(), tabs=[mock.Mock()])

    def test_forwards_self_and_events_to_tabs(self):
        self.assertEqual(self.editor.tabs[0].editor, self.editor)
