import unittest

from fitness.alignment_calculation import *
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel

from test.test_util import string_to_events, events_to_char_list


class AlignmentCalculationTest(unittest.TestCase):

    def test_nw_with_wrapper(self):
        event_group = EventGroup(string_to_events('pqacezxys'))

        result, model_result = nw_wrapper(event_group, 'zxabcdezx')
        self.assertEqual(-8, result)
        self.assertCountEqual([x for x in 'acezx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel(self):
        event_group = EventGroupParallel(string_to_events('pqacezxys'))

        result, model_result = nw_wrapper(event_group, 'zxklmnozx')
        self.assertEqual(-14, result)
        self.assertCountEqual([x for x in 'zx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_model_bigger(self):
        event_group_events = []
        for x in 'pqacezxysabc':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        result, model_result = nw_wrapper(event_group, 'zxabcdezx')
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'acezx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_log_bigger(self):
        event_group_events = []
        for x in 'pqacezxys':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        result, model_result = nw_wrapper(event_group, 'zxabcdezxabc')
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'acezx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside(self):
        event_group = EventGroupParallel([Event('t'), EventGroupParallel(string_to_events('spqacezxy'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezt')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in 'acezxt'], char_list)

    def test_nw_with_wrapper_parallel_inside_2(self):
        event_group = EventGroup([Event('t'),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezx')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-10, result)
        self.assertCountEqual([x for x in 'acezx'], char_list)

    def test_nw_with_wrapper_parallel_inside_3(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'acezq'], char_list)

    def test_nw_with_wrapper_parallel_inside_4(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel(string_to_events('tpq')),
                                          EventGroup(string_to_events('acez')),
                                          EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in 'acezxq'], char_list)

    def test_nw_with_wrapper_parallel_inside_5(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-6, result)
        self.assertCountEqual([x for x in 'acez'], char_list)

    def test_nw_with_wrapper_parallel_inside_6(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        result, model_result = nw_wrapper(event_group, 'zxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-5, result)
        self.assertCountEqual([x for x in 'z'], char_list)

    def test_nw_with_wrapper_parallel_inside_7(self):
        event_group = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])

        result, model_result = nw_wrapper(event_group, 'q')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-2, result)
        self.assertCountEqual([x for x in 'q'], char_list)

    def test_nw_with_wrapper_parallel_inside_72(self):
        event_group = EventGroup([Event('q'), EventGroupParallel(string_to_events('tp'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'q'], char_list)

    def test_nw_with_wrapper_parallel_inside_73(self):
        event_group = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'q'], char_list)

    def test_nw_with_wrapper_parallel_inside_74(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup([EventGroupParallel(string_to_events('ac')),
                                              EventGroup(string_to_events('ez'))])])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in 'acez'], char_list)

    def test_nw_with_wrapper_parallel_inside_75(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup([EventGroupParallel(string_to_events('ac')),
                                              EventGroup(string_to_events('ez'))]),
                                  EventGroupParallel(string_to_events('xys')),
                                  EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in 'acezxq'], char_list)

    def test_nw_with_wrapper_parallel_inside_8(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')]),
                                          EventGroup([EventGroupParallel(string_to_events('ac')),
                                                      EventGroup(string_to_events('ez'))]),
                                          EventGroupParallel(string_to_events('xys'))])

        result, model_result = nw_wrapper(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in 'acezxq'], char_list)

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
