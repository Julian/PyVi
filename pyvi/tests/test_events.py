from unittest import TestCase

import mock

from pyvi import editor, events, window
from pyvi.modes import insert


class TestEvents(TestCase):
    def test_insert_event(self):
        m = mock.Mock()
        insert.keypress(m, "i")

        self.assertEqual(
            m.events.trigger.call_args_list,
            [
                mock.call(event=events.INSERT_CHAR_PRE, char="i"),
                mock.call(event=events.INSERT_CHAR, char="i"),
            ]
        )
