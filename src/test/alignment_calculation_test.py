import unittest

from fitness.alignment_calculation import *
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel


def string_to_events(string: str):
    event_group_events = []
    for x in string:
        event_group_events.append(Event(x))
    return event_group_events


class AlignmentCalculationTest(unittest.TestCase):

    # def test_nw_with_wrapper_move_model(self):
    #
    #     self.assertEqual(nw_wrapper('zxabcdezx', 'pqacezxys'), -6)
    #     self.assertEqual(nw_wrapper('abcde', 'acezx'), -6)
    #     self.assertEqual(nw_wrapper('bcdez', 'acezx'), -6)
    #     self.assertEqual(nw_wrapper('cdezx', 'acezx'), -6)
    #
    #     nw_wrapper('zxabcdezx', 'pqacezxys')
    #     nw_wrapper('abcde', 'acezx')
    #     nw_wrapper('bcdez', 'acezx')
    #     nw_wrapper('cdezx', 'acezx')

    def test_nw_with_wrapper(self):
        event_group = EventGroup(string_to_events('pqacezxyx'))

        self.assertEqual(nw_wrapper('zxabcdezx', event_group), -8)

    def test_nw_with_wrapper_parallel(self):
        event_group = EventGroupParallel(string_to_events('pqacezxyx'))

        self.assertEqual(nw_wrapper('zxabcdezx', event_group), -6)

    def test_nw_with_wrapper_model_bigger(self):
        event_group_events = []
        for x in 'pqacezxyxabc':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        self.assertEqual(nw_wrapper('zxabcdezx', event_group), -11)

    def test_nw_with_wrapper_log_bigger(self):
        event_group_events = []
        for x in 'pqacezxyx':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        self.assertEqual(nw_wrapper('zxabcdezxabc', event_group), -11)

    def test_nw_with_wrapper_parallel_inside(self):
        event_group_events = []

        for x in 'tpqacezxyx':
            event_group_events.append(Event(x))
        event_group = EventGroupParallel([Event('t'), EventGroupParallel(event_group_events)])

        self.assertEqual(nw_wrapper('zxabcdezx', event_group), -7)
        # nw_wrapper('zxabcdezxq', event_group)

    def test_nw_with_wrapper_parallel_inside_2(self):
        event_group = EventGroup([Event('t'),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('xyx'))])

        # self.assertEqual(nw_wrapper('zxabcdezx', event_group), -8)
        nw_wrapper('zxabcdezxq', event_group)

    def test_nw_with_wrapper_parallel_inside_3(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel(string_to_events('tpq')),
                                          EventGroup(string_to_events('acez')),
                                          EventGroupParallel(string_to_events('xyx'))])

        self.assertEqual(nw_wrapper('zxabcdezxq', event_group), -8)
        # nw_wrapper('zxabcdezxq', event_group)

    def test_nw_with_wrapper_parallel_inside_4(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')]),
                                          EventGroup([EventGroupParallel(string_to_events('ac')),
                                                      EventGroup(string_to_events('ez'))]),
                                          EventGroupParallel(string_to_events('xyx'))])

        # self.assertEqual(nw_wrapper('zxabcdezx', event_group), -8)
        nw_wrapper('zxabcdezxq', event_group)

    def test_fill_result_matrix(self):
        matrix = [[0, -1, -2], [-1, 0, -1], [-2, -1, 0]]

    def test_resolve_parallel(self):
        True


if __name__ == '__main__':
    unittest.main()
