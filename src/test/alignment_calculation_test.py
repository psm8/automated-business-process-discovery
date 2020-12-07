import unittest

from fitness.alignment_calculation import *
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel

from test.test_util import string_to_events


class AlignmentCalculationTest(unittest.TestCase):

    # def test_nw_with_wrapper_move_model(self):
    #
    #     # self.assertEqual(nw_wrapper('zxabcdezx', 'pqacezxys'), -6)
    #     # self.assertEqual(nw_wrapper('abcde', 'acezx'), -6)
    #     # self.assertEqual(nw_wrapper('bcdez', 'acezx'), -6)
    #     # self.assertEqual(nw_wrapper('cdezx', 'acezx'), -6)
    #
    #     nw_wrapper('zxabcdezx', 'pqacezxys')
    #     nw_wrapper('abcde', 'acezx')
    #     nw_wrapper('bcdez', 'acezx')
    #     nw_wrapper('cdezx', 'acezx')

    def test_nw_with_wrapper(self):
        event_group = EventGroup(string_to_events('pqacezxys'))

        self.assertEqual(-8, nw_wrapper(event_group, 'zxabcdezx'))

    def test_nw_with_wrapper_parallel(self):
        event_group = EventGroupParallel(string_to_events('pqacezxys'))

        # self.assertEqual(nw_wrapper('zxabcdezx', event_group), -8)
        self.assertEqual(-14, nw_wrapper(event_group, 'zxklmnozx'))

    def test_nw_with_wrapper_model_bigger(self):
        event_group_events = []
        for x in 'pqacezxysabc':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        self.assertEqual(-11, nw_wrapper(event_group, 'zxabcdezx'))

    def test_nw_with_wrapper_log_bigger(self):
        event_group_events = []
        for x in 'pqacezxys':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        self.assertEqual(-11, nw_wrapper(event_group, 'zxabcdezxabc'))

    def test_nw_with_wrapper_parallel_inside(self):
        event_group = EventGroupParallel([Event('t'), EventGroupParallel(string_to_events('spqacezxy'))])

        self.assertEqual(-7, nw_wrapper(event_group, 'zxabcdezt'))
        # nw_wrapper('zxabcdezxq', event_group)

    def test_nw_with_wrapper_parallel_inside_2(self):
        event_group = EventGroup([Event('t'),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('xys'))])

        self.assertEqual(-10, nw_wrapper(event_group, 'zxabcdezx'))
        # nw_wrapper('zxabcdezxq', event_group)

    def test_nw_with_wrapper_parallel_inside_3(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroupParallel(string_to_events('xys'))])

        self.assertEqual(-11, nw_wrapper(event_group, 'zxabcdezxq'))
        # nw_wrapper('zxabcdezxq', event_group)

    def test_nw_with_wrapper_parallel_inside_4(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel(string_to_events('tpq')),
                                          EventGroup(string_to_events('acez')),
                                          EventGroupParallel(string_to_events('xys'))])

        self.assertEqual(-9, nw_wrapper(event_group, 'zxabcdezxq'))
        # nw_wrapper('zxabcdezxq', event_group)

    def test_nw_with_wrapper_parallel_inside_5(self):
        event_group = EventGroup([Event('t'),
                                          EventGroup([EventGroupParallel(string_to_events('ac')),
                                                      EventGroup(string_to_events('ez'))]),
                                          EventGroupParallel(string_to_events('xys')),
                                          EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])])


        self.assertEqual(-9, nw_wrapper(event_group, 'zxabcdezxq'))

    def test_nw_with_wrapper_parallel_inside_6(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])

        self.assertEqual(-6, nw_wrapper(event_group, 'zxabcdezxq'))

    def test_nw_with_wrapper_parallel_inside_7(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')]),
                                          EventGroup([EventGroupParallel(string_to_events('ac')),
                                                      EventGroup(string_to_events('ez'))]),
                                          EventGroupParallel(string_to_events('xys'))])

        self.assertEqual(-9, nw_wrapper(event_group, 'zxabcdezxq'))

    def test_fill_result_matrix(self):
        matrix = [[0, -1, -2], [-1, 0, -1], [-2, -1, 0]]

    def test_resolve_parallel(self):
        True


if __name__ == '__main__':
    unittest.main()
