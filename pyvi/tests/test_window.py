import collections
from unittest import TestCase

import mock

from pyvi import window


class TestBuffer(TestCase):
    def test_empty_buffer_is_empty(self):
        b = window.Buffer()
        self.assertEqual(len(b), 0)
        self.assertEqual(list(b), [])

    def test_get_line_by_index(self):
        lines = [u"foo\n", u"bar\n", u"baz\n"]
        b = window.Buffer(lines)
        self.assertEqual(b[0], lines[0])

    def test_set_line_by_index(self):
        lines = [u"foo\n", u"bar\n", u"baz\n"]
        b = window.Buffer(lines)

        b[1] = lines[1] = u"quux\n"
        self.assertEqual(list(b), lines)

    def test_cannot_set_slice(self):
        b = window.Buffer()
        with self.assertRaises(TypeError):
            b[:2] = [u"foo\n", u"bar\n"]

    def test_seeks_forward_for_unread_lines(self):
        b = window.Buffer((unicode(i) for i in xrange(100)))
        self.assertEqual(b.lines_read, 0)
        self.assertEqual(b[:10], [unicode(i) for i in xrange(10)])

        self.assertEqual(b.lines_read, 10)
        self.assertEqual(b[10], u"10")
        self.assertEqual(b.lines_read, 11)


class TestWindow(TestCase):
    def test_each_window_creates_a_buffer_partition_for_its_cursor(self):
        b = mock.Mock(_lines=[collections.deque()])
        w1 = window.Window(b)
        w2 = window.Window(b)
