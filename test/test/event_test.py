import unittest

from processdiscovery.event.event import Event
from processdiscovery.event.event_group import EventGroup
from processdiscovery.event.event_group_parallel import EventGroupParallel
from test.util.test_util import string_to_events


class EventTest(unittest.TestCase):

    def test_eq1(self):
        e1 = EventGroup([Event('f'), EventGroupParallel([Event('b'),
                                                         EventGroup(string_to_events('ccc'))])])
        e2 = EventGroup([Event('f'), EventGroupParallel([Event('b'),
                                                         EventGroup(string_to_events('ccc'))])])
        self.assertTrue(e1 == e2)

    def test_eq2(self):
        e1 = EventGroup([Event('f'), EventGroupParallel([Event('b'),
                                                         EventGroup(string_to_events('ccc'))])])
        e2 = EventGroupParallel([Event('f'), EventGroupParallel([Event('b'),
                                                                 EventGroup(string_to_events('ccc'))])])
        self.assertFalse(e1 == e2)

    def test_eq3(self):
        e1 = EventGroup([Event('f'), EventGroupParallel([Event('b'),
                                                         EventGroup(string_to_events('ccc'))])])
        e2 = EventGroupParallel([Event('f'), EventGroup([Event('b'),
                                                         EventGroup(string_to_events('cc'))])])
        self.assertFalse(e1 == e2)

    def test_eq4(self):
        e1 = EventGroup([Event('f'), EventGroupParallel([Event('b'),
                                                         EventGroup(string_to_events('ccc'))])])
        e2 = EventGroupParallel([Event('f'), EventGroup([Event('b'),
                                                         EventGroupParallel(string_to_events('ccc'))])])
        self.assertFalse(e1 == e2)


if __name__ == '__main__':
    unittest.main()
