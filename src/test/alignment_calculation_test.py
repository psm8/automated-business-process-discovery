import unittest

from fitness.alignment_calculation import *
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel

from test.test_util import string_to_events, events_to_char_list


class AlignmentCalculationTest(unittest.TestCase):

    def test_nw_with_wrapper(self):
        event_group = EventGroup(string_to_events('pqacezxys'))

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezx')
        self.assertEqual(-8, result)
        self.assertCountEqual([x for x in 'acezx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel(self):
        event_group = EventGroupParallel(string_to_events('pqacezxys'))

        result, model_result = calculate_best_alignment(event_group, 'zxklmnozx')
        self.assertEqual(-14, result)
        self.assertCountEqual([x for x in 'zx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_model_bigger(self):
        event_group_events = []
        for x in 'pqacezxysabc':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezx')
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'acezx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_log_bigger(self):
        event_group_events = []
        for x in 'pqacezxys':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxabc')
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'acezx'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside(self):
        event_group = EventGroupParallel([Event('t'), EventGroupParallel(string_to_events('spqacezxy'))])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezt')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in 'acezxt'], char_list)

    def test_nw_with_wrapper_parallel_inside_2(self):
        event_group = EventGroup([Event('t'),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('xys'))])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezx')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-10, result)
        self.assertCountEqual([x for x in 'acezx'], char_list)

    def test_nw_with_wrapper_parallel_inside_3(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroupParallel(string_to_events('xys'))])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'acezq'], char_list)

    def test_nw_with_wrapper_parallel_inside_4(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel(string_to_events('tpq')),
                                          EventGroup(string_to_events('acez')),
                                          EventGroupParallel(string_to_events('xys'))])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in 'acezxq'], char_list)

    def test_nw_with_wrapper_parallel_inside_5(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-6, result)
        self.assertCountEqual([x for x in 'acez'], char_list)

    def test_nw_with_wrapper_parallel_inside_6(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        result, model_result = calculate_best_alignment(event_group, 'zxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-5, result)
        self.assertCountEqual([x for x in 'z'], char_list)

    def test_nw_with_wrapper_parallel_inside_7(self):
        event_group = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])

        result, model_result = calculate_best_alignment(event_group, 'q')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-2, result)
        self.assertCountEqual([x for x in 'q'], char_list)

    def test_nw_with_wrapper_parallel_inside_72(self):
        event_group = EventGroup([Event('q'), EventGroupParallel(string_to_events('tp'))])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'q'], char_list)

    def test_nw_with_wrapper_parallel_inside_73(self):
        event_group = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in 'q'], char_list)

    def test_nw_with_wrapper_parallel_inside_74(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup([EventGroupParallel(string_to_events('ac')),
                                              EventGroup(string_to_events('ez'))])])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in 'acez'], char_list)

    def test_nw_with_wrapper_parallel_inside_75(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup([EventGroupParallel(string_to_events('ac')),
                                              EventGroup(string_to_events('ez'))]),
                                  EventGroupParallel(string_to_events('xys')),
                                  EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in 'acezxq'], char_list)

    def test_nw_with_wrapper_parallel_inside_8(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')]),
                                          EventGroup([EventGroupParallel(string_to_events('ac')),
                                                      EventGroup(string_to_events('ez'))]),
                                          EventGroupParallel(string_to_events('xys'))])

        result, model_result = calculate_best_alignment(event_group, 'zxabcdezxq')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in 'acezxq'], char_list)

    def test_nw_with_wrapper_parallel_inside_9(self):
        event_group = EventGroup([Event('f'),
                                  EventGroupParallel([EventGroupParallel(string_to_events('dc')), Event('f')]),
                                  Event('b'),
                                  EventGroupParallel([EventGroupParallel(string_to_events('df')), Event('e')])])

        result, model_result = calculate_best_alignment(event_group, 'acbd')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-6, result)
        self.assertCountEqual([x for x in 'bcd'], char_list)

    def test_additional0(self):
        event_group = EventGroup([Event('f'),
                                  EventGroup([EventGroupParallel([EventGroup([Event('a')]), Event('f')]), Event('b')]),
                                  Event('f')])

        result, model_result = calculate_best_alignment(event_group, 'abcdef')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-5, result)
        self.assertCountEqual([x for x in 'abf'], char_list)

    def test_additional1(self):
        event_group = EventGroup([Event('f'),
                                  EventGroup([EventGroupParallel([Event('a'), Event('f')]), Event('b')]),
                                  Event('f')])

        result, model_result = calculate_best_alignment(event_group, 'abcdef')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-5, result)
        self.assertCountEqual([x for x in 'abf'], char_list)

    def test_additional2(self):
        event_group = EventGroup([Event('a'),
                                  EventGroup([Event('a'), Event('b'), Event('c'), Event('e'),
                                              EventGroup([Event('f'), Event('f')])]),
                                  Event('b'),
                                  Event('c')])

        result, model_result = calculate_best_alignment(event_group, 'acbd')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in 'abc'], char_list)

    def test_additional3(self):
        event_group = EventGroup([EventGroupParallel([Event('c'), Event('f')]),
                                  EventGroupParallel([Event('a'), Event('b')]),
                                  Event('c')])

        result, model_result = calculate_best_alignment(event_group, 'bcd')
        char_list = events_to_char_list(model_result)
        self.assertEqual(-4, result)
        self.assertCountEqual([x for x in 'bc'], char_list)

    def test_parallel_many_events(self):
        event_group = EventGroupParallel([EventGroupParallel([Event('a'), Event('b')]),
                                          Event('c'), Event('d'), Event('e'), Event('f'), Event('g'), Event('h'),
                                          Event('i'), Event('j'), Event('k'), Event('l'), Event('m'), Event('n')])

        result, model_result = calculate_best_alignment(event_group, 'abcdefghijklmn')
        char_list = events_to_char_list(model_result)
        self.assertEqual(0, result)
        self.assertCountEqual([x for x in 'abcdefghijklmn'], char_list)

    if __name__ == '__main__':
        unittest.main()
