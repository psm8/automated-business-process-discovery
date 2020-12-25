import unittest

from processdiscovery.event.event import Event
from processdiscovery.event.event_group import EventGroup
from processdiscovery.event.event_group_parallel import EventGroupParallel
from processdiscovery.test.util.test_util import string_to_events
from processdiscovery.util.util import flatten_values, event_list_length, subset_sum, to_n_length, to_n_length_old

from itertools import product
from copy import deepcopy
from timeit import default_timer as timer


class UtilTest(unittest.TestCase):

    def test_min_event_list_length_test(self):
        e1 = Event('t')
        e2 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
        e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e4 = EventGroupParallel(string_to_events('xys'))

        test_list = [[[e1], [e2, e3], [e4, e1, e2]], [[e3, e4, e1], [e2], [e3, e4]]]
        expected = 2
        actual = event_list_length(test_list, min)

        self.assertEqual(expected, actual)

    def test_max_event_list_length_test(self):
        e1 = Event('t')
        e2 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
        e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e4 = EventGroupParallel(string_to_events('xys'))

        test_list = [[[e1], [e2, e3], [e4, e1, e2]], [[e3, e4, e1], [e2], [e3, e4]]]
        expected = 8
        actual = event_list_length(test_list, max)

        self.assertEqual(expected, actual)

    def test_flatten_values(self):
        e1 = Event('t')
        e2 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
        e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e4 = EventGroupParallel(string_to_events('xys'))
        e5 = Event('t')
        e6 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
        e7 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e8 = EventGroupParallel(string_to_events('xys'))
        e9 = Event('t')
        e10 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
        e11 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e12 = EventGroupParallel(string_to_events('xys'))
        e13 = Event('t')

        expected_1 = [list(x) for x in product([e1, e2, e3, e4, e5, e6], [e7, e8, e9, e10, e11, e12])]
        expected_2 = deepcopy(expected_1)
        [x.append(e13) for x in expected_2]
        expected = expected_1 + expected_2
        actual = flatten_values([[[e1], [e2, e3], [e4, e5, e6]], [[e7, e8, e9], [e10], [e11, e12]], [[e13], []]])
        self.assertCountEqual(expected, actual)

    def test_to_n_length(self):
        e1 = Event('t')
        e2 = EventGroupParallel([EventGroupParallel(string_to_events('t')), Event('q')])
        e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e4 = EventGroupParallel(string_to_events('xys'))

        expected = [EventGroup([e1, e1, e2]), EventGroup([e1, e2, e1]), EventGroup([e2, e1, e1]),
                    EventGroup([e4, e1]), EventGroup([e1, e4]), EventGroup([e2, e2]), e3]
        actual = to_n_length(4, [e1, e2, e3, e4], 3)
        self.assertEqual(len(expected), len(actual))

    def test_to_n_length_2(self):
        e1 = Event('t')
        e2 = EventGroupParallel([EventGroupParallel(string_to_events('t')), Event('q')])
        e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e4 = EventGroupParallel(string_to_events('xys'))
        e5 = Event('t')
        e6 = EventGroupParallel([EventGroupParallel(string_to_events('t')), Event('q')])
        e7 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e8 = EventGroupParallel(string_to_events('xys'))
        e9 = Event('t')
        e10 = EventGroupParallel([EventGroupParallel(string_to_events('t')), Event('q')])
        e11 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e12 = EventGroupParallel(string_to_events('xys'))
        e13 = Event('h')
        e14 = Event('h')
        e15 = Event('h')
        e16 = Event('i')
        e17 = Event('i')
        e18 = Event('i')
        e19 = Event('j')
        e20 = Event('j')
        e21 = Event('j')

        start = timer()
        for i in range(100):
            actual = to_n_length(4, [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18,
                                     e19, e20, e21], 4)
        end = timer()
        print(end - start)

        self.assertEqual(22116, len(actual))

        start = timer()
        for i in range(100):
            actual_old = to_n_length_old(4, [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17,
                                             e18, e19, e20, e21], 4)
        end = timer()
        print(end - start)

        self.assertEqual(22116, len(actual_old))

    def test_subset_sum(self):
        v = [1, 1, 2, 3, 10]
        sum = 12
        print(list(subset_sum(v, sum)))

if __name__ == '__main__':
    unittest.main()
