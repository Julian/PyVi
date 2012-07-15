from StringIO import StringIO
from unittest import TestCase

import mock

from pyvi import editor, window
from pyvi.tests.util import MockCursor


class TestBuffer(TestCase):
    def test_empty_buffer_has_one_empty_line(self):
        b = window.Buffer()
        self.assertEqual(len(b), 1)
        self.assertEqual(list(b), [u""])

    def test_iter(self):
        lines = [u"foo", u"bar", u"baz"]
        b = window.Buffer(lines)
        self.assertEqual(list(iter(b)), lines)

    def test_write(self):
        s = StringIO()
        b = window.Buffer(unicode(i) for i in xrange(10))
        b.write(s)
        self.assertEqual(
            s.getvalue(), u"\n".join(map(unicode, xrange(10))) + u"\n"
        )


class TestBufferLinewise(TestCase):
    def setUp(self):
        self.lines = [u"foo", u"bar", u"baz", u"quux", u"spam", u"eggs"]
        self.buffer = window.Buffer(self.lines)

    def test_equal_to_list_like_stuff(self):
        self.assertEqual(self.buffer.lines, self.lines)
        self.assertNotEqual(self.buffer.lines, [])

    def test_iterate_over_lines(self):
        self.assertEqual(list(self.buffer.lines), self.lines)

    def test_get_line_by_index(self):
        self.assertEqual(self.buffer.lines[0], self.lines[0])

    # XXX: Slice step
    def test_get_slice(self):
        self.assertEqual(self.buffer.lines[1:5], self.lines[1:5])

    def test_get_open_slice(self):
        self.assertEqual(self.buffer.lines[1:], self.lines[1:])

    def test_no_such_line_raises_IndexError(self):
        with self.assertRaises(IndexError):
            self.buffer.lines[1000]

        with self.assertRaises(IndexError):
            self.buffer.lines[1000] = u"foo"

    def test_set_line_by_index(self):
        self.buffer.lines[1] = self.lines[1] = u"monty"
        self.assertEqual(self.buffer.lines, self.lines)

    def test_set_slice(self):
        self.buffer.lines[:3] = self.lines[:3] = [u"oof", u"rab", u"zab"]
        self.assertEqual(self.buffer.lines, self.lines)


class TestBufferSeek(TestCase):
    def test_seeks_forward_for_unread_lines(self):
        b = window.Buffer((unicode(i) for i in xrange(100)))
        self.assertEqual(b.lines_read, 0)
        self.assertEqual(b[:10], [unicode(i) for i in xrange(10)])

        self.assertEqual(b.lines_read, 10)
        self.assertEqual(b[10], u"10")
        self.assertEqual(b.lines_read, 11)


class TestBufferCharwise(TestCase):
    def setUp(self):
        self.lines = [u"foo", u"bar", u"baz", u"quux", u"spam", u"eggs"]
        self.chars = "\n".join(self.lines)
        self.buffer = window.Buffer(self.lines)

    def test_equal_to_str_like_stuff(self):
        self.assertEqual(self.buffer.chars, self.chars)
        self.assertNotEqual(self.buffer.chars, u"")

    def test_str(self):
        self.assertEqual(str(self.buffer.chars), self.chars)

    def test_len(self):
        self.assertEqual(len(self.buffer.chars), len(self.chars))

    def test_iterate_over_chars(self):
        self.assertEqual(list(self.buffer.chars), list(self.chars))

    # We'll see later whether we need these or not (arbitrary access)
    # def test_get_char_by_index(self):
    #     self.assertEqual(self.buffer.chars[0], self.chars[0])

    # def test_get_slice(self):
    #     self.assertEqual(self.buffer.chars[1:5], self.chars[1:5])

    # def test_get_open_slice(self):
    #     self.assertEqual(self.buffer.chars[1:], self.chars[1:])

    # def test_no_such_char_raises_IndexError(self):
    #     with self.assertRaises(IndexError):
    #         self.buffer.chars[1000000]


class TestBufferDelegatesToLines(TestCase):
    def setUp(self):
        self.buffer = window.Buffer()
        self.buffer.lines = self.m = mock.MagicMock()

    def test_get_line(self):
        self.buffer[2]
        self.m.__getitem__.assert_called_once_with(2)

    def test_set_line(self):
        self.buffer[2] = u"foo"
        self.m.__setitem__.assert_called_once_with(2, u"foo")

    def test_iter(self):
        iter(self.buffer)
        self.m.__iter__.assert_called_once_with()

    def test_len(self):
        len(self.buffer)
        self.m.__len__.assert_called_once_with()

    def test_lines_read(self):
        # This is a property, but who cares, we can call it
        self.buffer.lines_read()
        self.m.lines_read.assert_called_once_with()


class TestBufferCursor(TestCase):
    def setUp(self):
        self.lines = [u"foo", u"bar", u"baz"]
        self.buffer = window.Buffer(self.lines)
        self.window = mock.Mock()
        self.buffer.cursors[self.window] = self.cursor = MockCursor()

    def test_insert(self):
        self.buffer.insert(self.window, u"fo")
        self.assertEqual(self.cursor.row, 0)
        self.assertEqual(self.cursor.column, 2)

        self.buffer.insert(self.window, u"o")
        self.assertEqual(self.cursor.row, 0)
        self.assertEqual(self.cursor.column, 3)

        self.buffer.insert(self.window, u"bar", u"baz", u"quux")
        self.assertEqual(self.cursor.row, 2)
        self.assertEqual(self.cursor.column, 4)

        self.buffer.insert(self.window, u"", u"")
        self.assertEqual(self.cursor.row, 3)
        self.assertEqual(self.cursor.column, 0)

        self.assertEqual(
            list(self.buffer), [u"foobar", u"baz", u"quux"] + self.lines,
        )


class TestWindow(TestCase):
    def setUp(self):
        self.editor = mock.Mock()
        self.buffer = mock.MagicMock()
        self.window = window.Window(self.editor, self.buffer)
        self.cursor = self.window.cursor

    def test_cursor_trim(self):
        self.buffer.__len__.return_value = 6
        self.buffer[5].__len__.return_value = 4
        self.window.cursor.coords = (8, 10)
        self.window.cursor.trim()
        self.assertEqual(self.window.cursor.coords, (5, 3))

    def test_chars(self):
        self.window.chars()
        self.buffer.chars.assert_called_once_with(start=self.cursor.coords)

    def test_delete(self):
        self.window.delete()
        self.buffer.delete.assert_called_once_with(start=self.cursor.coords)


class TestTab(TestCase):
    def setUp(self):
        self.editor = mock.Mock()
        self.windows = [[mock.Mock(), mock.Mock()], [mock.Mock(), mock.Mock()]]
        self.tab = window.Tab(editor=self.editor, windows=self.windows)

    def test_active_window(self):
        tab = window.Tab(self.editor)
        self.assertEqual(tab.active_window, tab.windows[0][0])

    def test_iter_returns_rows(self):
        first, second = list(self.tab)
        self.assertEqual(first, self.windows[0])
        self.assertEqual(second, self.windows[1])



class TestEditor(TestCase):
    def setUp(self):
        self.editor = editor.Editor(config=mock.Mock(), tabs=[mock.Mock()])

    def test_handle_next_key(self):
        m = mock.Mock()
        self.editor.keypress("z")
        self.editor.next_keyhandler = m
        self.editor.keypress("z")
        m.assert_called_once_with("z")

    def test_handle_next_key_reset(self):
        def handle(key):
            if key == "r":
                self.editor.next_keyhandler = handle

        self.editor.next_keyhandler = handle
        self.editor.keypress("z")
        self.assertNotEqual(self.editor.next_keyhandler, handle)

        self.editor.next_keyhandler = handle
        self.editor.keypress("r")
        self.assertEqual(self.editor.next_keyhandler, handle)
