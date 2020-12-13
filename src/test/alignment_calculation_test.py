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

        result, model_result = nw_wrapper(event_group, 'zxabcdezx')
        self.assertEqual(-8, result)

    def test_nw_with_wrapper_parallel(self):
        event_group = EventGroupParallel(string_to_events('pqacezxys'))

        result, model_result = nw_wrapper(event_group, 'zxklmnozx')
        self.assertEqual(-14, result)

    def test_nw_with_wrapper_model_bigger(self):
        event_group_events = []
        for x in 'pqacezxysabc':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        result, model_result = nw_wrapper(event_group, 'zxabcdezx')
        self.assertEqual(-11, result)

    def test_nw_with_wrapper_log_bigger(self):
        event_group_events = []
        for x in 'pqacezxys':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        result, model_result = nw_wrapper(event_group, 'zxabcdezxabc')
        self.assertEqual(-11, result)

    def test_nw_with_wrapper_parallel_inside(self):
        event_group = EventGroupParallel([Event('t'), EventGroupParallel(string_to_events('spqacezxy'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezt')
        self.assertEqual(-7, result)

    def test_nw_with_wrapper_parallel_inside_2(self):
        event_group = EventGroup([Event('t'),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezx')
        self.assertEqual(-10, result)

    def test_nw_with_wrapper_parallel_inside_3(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        self.assertEqual(-11, result)

    def test_nw_with_wrapper_parallel_inside_4(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel(string_to_events('tpq')),
                                          EventGroup(string_to_events('acez')),
                                          EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        self.assertEqual(-9, result)

    def test_nw_with_wrapper_parallel_inside_5(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        self.assertEqual(-6, result)

    def test_nw_with_wrapper_parallel_inside_6(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        result, model_result = nw_wrapper(event_group, 'zxq')
        self.assertEqual(-5, result)

    def test_nw_with_wrapper_parallel_inside_7(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup([EventGroupParallel(string_to_events('ac')),
                                              EventGroup(string_to_events('ez'))]),
                                  EventGroupParallel(string_to_events('xys')),
                                  EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        self.assertEqual(-9, result)

    def test_nw_with_wrapper_parallel_inside_8(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        self.assertEqual(-6, result)

    def test_nw_with_wrapper_parallel_inside_9(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')]),
                                          EventGroup([EventGroupParallel(string_to_events('ac')),
                                                      EventGroup(string_to_events('ez'))]),
                                          EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        self.assertEqual(-9, result)

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

        expected = [[e1, e7, e8, e9, e13], [e1, e10, e13], [e1, e11, e12, e13], [e2, e3, e7, e8, e9, e13],
                    [e2, e3, e10, e13], [e2, e3, e11, e12, e13], [e4, e5, e6, e7, e8, e9, e13],
                    [e4, e5, e6, e10, e13], [e4, e5, e6, e11, e12, e13]]
        self.assertEqual(expected, flatten_values([[[e1], [e2, e3], [e4, e5, e6]],
                                                   [[e7, e8, e9], [e10], [e11, e12]],
                                                   [[e13]]]))

    if __name__ == '__main__':
        unittest.main()
