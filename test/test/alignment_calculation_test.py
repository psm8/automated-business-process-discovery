import unittest

from process_discovery.evaluation.alignment_calculation.alignment_calculation import *
from process_discovery.evaluation.alignment_calculation.cache import *
from process_discovery.event.event import Event
from process_discovery.event.event_group import EventGroup
from process_discovery.event.event_group_parallel import EventGroupParallel

from test.util.test_util import string_to_events, events_to_char_list


class AlignmentCalculationTest(unittest.TestCase):

    def test_nw_with_wrapper(self):
        event_group = EventGroup(string_to_events('pqacezxys'))

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x'], dict())
        print(events_to_char_list(model_result))
        self.assertEqual(-8, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'x']], events_to_char_list(model_result))
        self.assertEqual(['a', 'c', 'e', 'z', 'x'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel(self):
        event_group = EventGroupParallel(string_to_events('pqacezxys'))

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'k', 'l', 'm', 'n', 'o', 'z', 'x'], dict())
        print(events_to_char_list(model_result))
        self.assertEqual(-14, result)
        self.assertCountEqual([x for x in ['z', 'x']], events_to_char_list(model_result))
        self.assertEqual(['z', 'x'], events_to_char_list(model_result))

    def test_nw_with_wrapper_model_bigger(self):
        event_group_events = []
        for x in 'pqacezxysabc':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z',
                                                                                 'x'], dict())
        print(events_to_char_list(model_result))
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'x']], events_to_char_list(model_result))
        self.assertEqual(['a', 'c', 'e', 'z', 'x'], events_to_char_list(model_result))

    def test_nw_with_wrapper_log_bigger(self):
        event_group_events = []
        for x in 'pqacezxys':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['z', 'x', 'a', 'b', 'c', 'd', 'e',
                                                                                 'z', 'x', 'a', 'b', 'c'], dict())
        print(events_to_char_list(model_result))
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'x']], events_to_char_list(model_result))
        self.assertEqual(['a', 'c', 'e', 'z', 'x'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside(self):
        event_group = EventGroupParallel([Event('t'), EventGroupParallel(string_to_events('spqacezxy'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z',
                                                                                 't'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in ['z', 'x', 'a', 'c', 'e', 't']], char_list)
        self.assertEqual(['z', 'x', 'a', 'c', 'e', 't'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_2(self):
        event_group = EventGroup([Event('t'),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('xys'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z',
                                                                                 'x'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-10, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'x']], char_list)
        self.assertEqual(['a', 'c', 'e', 'z', 'x'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_3(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup(string_to_events('acez')),
                                  EventGroupParallel(string_to_events('tpq')),
                                  EventGroupParallel(string_to_events('xys'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'q']], char_list)
        self.assertEqual(['a', 'c', 'e', 'z', 'q'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_4(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel(string_to_events('tpq')),
                                          EventGroup(string_to_events('acez')),
                                          EventGroupParallel(string_to_events('xys'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'x', 'q']], char_list)
        self.assertEqual(['a', 'c', 'e', 'z', 'x', 'q'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_5(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-6, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z']], char_list)
        self.assertEqual(['a', 'c', 'e', 'z'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_6(self):
        event_group = EventGroup([EventGroupParallel(string_to_events('ac')),
                                  EventGroup(string_to_events('ez'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-5, result)
        self.assertCountEqual([x for x in ['z']], char_list)
        self.assertEqual(['z'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_7(self):
        event_group = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-2, result)
        self.assertCountEqual([x for x in ['q']], char_list)
        self.assertEqual(['q'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_72(self):
        event_group = EventGroup([Event('q'), EventGroupParallel(string_to_events('tp'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in ['q']], char_list)
        self.assertEqual(['q'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_73(self):
        event_group = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-11, result)
        self.assertCountEqual([x for x in ['q']], char_list)
        self.assertEqual(['q'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_74(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup([EventGroupParallel(string_to_events('ac')),
                                              EventGroup(string_to_events('ez'))])])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z']], char_list)
        self.assertEqual(['a', 'c', 'e', 'z'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_75(self):
        event_group = EventGroup([Event('t'),
                                  EventGroup([EventGroupParallel(string_to_events('ac')),
                                              EventGroup(string_to_events('ez'))]),
                                  EventGroupParallel(string_to_events('xys')),
                                  EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                         ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'x', 'q']], char_list)
        self.assertEqual(['a', 'c', 'e', 'z', 'x', 'q'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_8(self):
        event_group = EventGroupParallel([Event('t'),
                                          EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')]),
                                          EventGroup([EventGroupParallel(string_to_events('ac')),
                                                      EventGroup(string_to_events('ez'))]),
                                          EventGroupParallel(string_to_events('xys'))])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group,
                                                  ['z', 'x', 'a', 'b', 'c', 'd', 'e', 'z', 'x', 'q'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-9, result)
        self.assertCountEqual([x for x in ['a', 'c', 'e', 'z', 'x', 'q']], char_list)
        self.assertEqual(['a', 'c', 'e', 'z', 'x', 'q'], events_to_char_list(model_result))

    def test_nw_with_wrapper_parallel_inside_9(self):
        event_group = EventGroup([Event('f'),
                                  EventGroupParallel([EventGroupParallel(string_to_events('dc')), Event('f')]),
                                  Event('b'),
                                  EventGroupParallel([EventGroupParallel(string_to_events('df')), Event('e')])])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['a', 'c', 'b', 'd'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-6, result)
        self.assertCountEqual([x for x in ['c', 'b', 'd']], char_list)
        self.assertEqual(['c', 'b', 'd'], events_to_char_list(model_result))

    def test_additional0(self):
        event_group = EventGroup([Event('f'),
                                  EventGroup([EventGroupParallel([EventGroup([Event('a')]), Event('f')]), Event('b')]),
                                  Event('f')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['a', 'b', 'c', 'd', 'e', 'f'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-5, result)
        self.assertCountEqual([x for x in ['a', 'b', 'f']], char_list)
        self.assertEqual(['a', 'b', 'f'], events_to_char_list(model_result))

    def test_additional1(self):
        event_group = EventGroup([Event('f'),
                                  EventGroup([EventGroupParallel([Event('a'), Event('f')]), Event('b')]),
                                  Event('f')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['a', 'b', 'c', 'd', 'e', 'f'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-5, result)
        self.assertCountEqual([x for x in ['a', 'b', 'f']], char_list)
        self.assertEqual(['a', 'b', 'f'], events_to_char_list(model_result))

    def test_additional2(self):
        event_group = EventGroup([Event('a'),
                                  EventGroup([Event('a'), Event('b'), Event('c'), Event('e'),
                                              EventGroup([Event('f'), Event('f')])]),
                                  Event('b'),
                                  Event('c')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['a', 'c', 'b', 'd'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-7, result)
        self.assertCountEqual([x for x in ['a', 'b', 'c']], char_list)
        self.assertEqual(['a', 'c', 'b'], events_to_char_list(model_result))

    def test_additional3(self):
        event_group = EventGroup([EventGroupParallel([Event('c'), Event('f')]),
                                  EventGroupParallel([Event('a'), Event('b')]),
                                  Event('c')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['b', 'c', 'd'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-4, result)
        self.assertCountEqual([x for x in ['b', 'c']], char_list)
        self.assertEqual(['b', 'c'], events_to_char_list(model_result))

    def test_legend(self):
        event_group = EventGroup([Event('a'), EventGroupParallel([Event('c'), Event('d')]),
                                  Event('e'), Event('h')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['a', 'c', 'd', 'e', 'h'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(0, result)
        self.assertCountEqual([x for x in ['a', 'c', 'd', 'e', 'h']], char_list)
        self.assertEqual(['a', 'c', 'd', 'e', 'h'], events_to_char_list(model_result))

    def test_all_events_in_model(self):
        # when your algorithm is smarter than you
        event_group = EventGroupParallel([Event('a'), Event('f'),
                                  EventGroupParallel(string_to_events('bec')),
                                  Event('d')])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['a', 'b', 'c', 'd', 'e', 'f'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-2, result)
        self.assertCountEqual([x for x in ['a', 'b', 'c', 'e', 'f']], char_list)

    def test_cache(self):
        event_group = [EventGroupParallel([Event('a'), Event('f'),
                                          EventGroupParallel(string_to_events('bec')),
                                          Event('d')])]
        event_group2 = [EventGroupParallel([Event('a'), Event('f'),
                                            EventGroupParallel(string_to_events('bec')),
                                            Event('d')])]
        log = ['a', 'b', 'c', 'd', 'e', 'f']
        log2 = ['a', 'b', 'c', 'd', 'e', 'f']
        cache1 = get_cache_id(event_group, log)
        cache2 = get_cache_id(event_group2, log2)
        self.assertEqual(cache1, cache2)

    def test_parallel_many_events(self):
        event_group = EventGroupParallel([EventGroupParallel([Event('a'), Event('b')]),
                                          # Event('c'), Event('d'), Event('e'), Event('f'), Event('g'),
                                          # Event('h'),
                                          # Event('i'),
                                          Event('j'),
                                          Event('k'),
                                          Event('l'), Event('m'), Event('n'),
                                          EventGroupParallel([Event('o'), Event('p'), Event('q')])])

        alignment_cached = BestAlignmentCached()
        result, model_result = alignment_cached.get_best_alignment(event_group, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                                                                 'i', 'j', 'k', 'l', 'm', 'n'], dict())
        char_list = events_to_char_list(model_result)
        print(events_to_char_list(model_result))
        self.assertEqual(-10, result)
        self.assertCountEqual([x for x in 'abcdefghijklmn'], char_list)
    #
    # def test_parallel_event_permutations(self):
    #     event_group = EventGroupParallel([EventGroupParallel([Event('a'), Event('b')]),
    #                                       Event('c'), Event('d'), Event('e'), Event('f'), Event('g'), Event('h'),
    #                                       Event('i'), Event('j'), Event('k'), Event('l'), Event('m'), Event('n'),
    #                                       EventGroupParallel([Event('o'), Event('p'), Event('q')])])
    #
    #     expected = parallel_event_permutations(event_group)


    if __name__ == '__main__':
        unittest.main()
