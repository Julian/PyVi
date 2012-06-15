from unittest import TestCase

import mock

from pyvi import editor, events, window
from pyvi.modes import insert, normal


class TestBufferWindowTabInteraction(TestCase):
    def setUp(self):
        self.editor = editor.Editor()
        self.tab = self.editor.active_tab
        self.window = self.tab.active_window
        self.buffer = self.window.buffer

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
        another = window.Window(self.editor, self.buffer, cursor=(2, 3))
        and_another = window.Window(self.editor, self.buffer, cursor=(0, 0))

        self.window.insert(u"spam")
        another.insert(u"", u"eggs")
        and_another.insert(u"cheese", u"")

        lines = [u"cheese", u"foo", u"bar", u"baz", u"eggs", u"quux", u"spam"]
        self.assertEqual(list(self.buffer), lines)

        self.assertEqual(self.window.cursor, (6, 4))
        self.assertEqual(another.cursor, (4, 4))
        self.assertEqual(and_another.cursor, (1, 0))


class TestEditorIntegration(TestCase):
    def setUp(self):
        self.editor = editor.Editor()
        self.tabs = self.editor.tabs
        self.tabs.append(window.Tab(self.editor))

    def test_insert_some_text_via_keypresses(self):
        self.assertEqual(self.editor.active_tab, self.tabs[0])
        self.assertEqual(self.editor.mode, normal)

        self.editor.keypress("i")
        self.assertEqual(self.editor.mode, insert)

        for key in u"foo":
            self.editor.keypress(key)

        self.assertEqual(self.editor.active_window.buffer[0], u"foo")
        self.assertEqual(self.editor.active_window.cursor, (0, 3))

        self.editor.keypress("esc")
        self.assertEqual(self.editor.mode, normal)


class TestEvents(TestCase):
    def setUp(self):
        self.editor = editor.Editor()
        self.tab = self.editor.active_tab
        self.window = self.tab.active_window

    def test_cursor_moved(self):
        test = mock.Mock(return_value=None)
        self.editor.events.subscribe(event=events.CURSOR_MOVED)(test)
        self.window.insert("foo")
        test.assert_called_once_with(mock.ANY)  # ANY = a pangler
