import unittest

from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.gate.and_gate import AndGate
from processdiscovery.event.event import Event
from processdiscovery.event.base_group import BaseGroup
from processdiscovery.event.event_group import EventGroup
from processdiscovery.event.event_group_parallel import EventGroupParallel
from processdiscovery.test.util.test_util import string_to_events

from math import pow


class GateTest(unittest.TestCase):

    def test_1(self):
        gate = SeqGate()
        gate.parse('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})')
        self.assertCountEqual([EventGroupMatcher(EventGroup([EventGroupParallel(string_to_events('abcdefghijklmn'))]))],
                              gate.get_all_n_length_routes(14, ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                                                                'l', 'm', 'n')))
        self.assertEqual([], gate.get_all_n_length_routes(13, ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                                                               'l', 'm', 'n')))

    def test_2(self):
        gate = SeqGate()
        gate.parse('{f}xor({d}and({b}lop({c})opt({a})))')

        actual = gate.get_all_n_length_routes(5)
        expected_1 = EventGroupMatcher(EventGroup([Event('f'), EventGroupParallel([Event('b'),
                                                                                   EventGroup(string_to_events('ccc'))])]))
        expected_2 = EventGroupMatcher(EventGroup([Event('f'), EventGroupParallel([Event('b'),
                                                                                   EventGroup(string_to_events('cc')),
                                                                                   Event('a')])]))
        expected = [expected_1, expected_2]
        self.assertCountEqual(expected, actual)

    def test_3(self):
        gate = SeqGate('lop(opt(seq(xor({e}{c})lop({d}))){f})')

    def test_4(self):
        gate = SeqGate('and(lop(opt(seq(xor({e}{c})lop({d}))){f}){a})and({d}{a})')

    def test_5(self):
        gate = SeqGate('lop(xor({b}xor({a}{e}{d})){e})')

    def test_6(self):
        gate = SeqGate()
        gate.parse('xor(and({c}and(and({c}{b}and({d}{f})){b}{e})){e}{e})')
        self.assertEqual([EventGroup([EventGroupParallel(string_to_events('abcdefghijklmn'))])], gate.get_all_n_length_routes(7))
        self.assertEqual([], gate.get_all_n_length_routes(6))

    def test_7(self):
        gate = SeqGate()
        gate.parse('lop({c})')
        self.assertEqual(None, gate.get_all_n_length_routes(6))
        self.assertEqual([EventGroupMatcher(EventGroup([EventGroupParallel(string_to_events('ccc'))]))],
                         gate.get_all_n_length_routes(3))

    def test_8(self):
        gate = SeqGate()
        gate.parse('xor({f}{d}and({e}xor(lop(xor({f}{d}))lop({a}))))and({b}{a})')
        all_length_3_routes = gate.get_all_n_length_routes(3)
        self.assertCountEqual([EventGroupMatcher(EventGroup([Event('f'), EventGroupParallel(string_to_events('ba'))])),
                               EventGroupMatcher(EventGroup([Event('d'), EventGroupParallel(string_to_events('ba'))])),
                               EventGroupMatcher(EventGroup([Event('e'), EventGroupParallel(string_to_events('ba'))]))],
                              all_length_3_routes)

    def test_9(self):
        gate = SeqGate()
        gate.parse('and({c}and({a}lop({e}opt({d}))seq({c}{b})))')
        all_length_5_routes = gate.get_all_n_length_routes(5)
        expected = [EventGroupMatcher(EventGroup([EventGroupParallel([Event('c'),
                                                                      EventGroupParallel([Event('a'),
                                                                                          Event('e'),
                                                                                          EventGroup(string_to_events('cb'))])])]))]
        self.assertCountEqual(expected, all_length_5_routes)

    def test_92(self):
        gate = SeqGate()
        gate.parse('and({a}{f}opt(and({b}{e}lop({c}))){d})')
        all_length_6_routes = gate.get_all_n_length_routes(6)
        expected = [EventGroupMatcher(EventGroup([EventGroupParallel([Event('a'), Event('f'),
                                                                      EventGroupParallel(string_to_events('bec')),
                                                                      Event('d')])]))]
        self.assertCountEqual(expected, all_length_6_routes)

    def test_93(self):
        gate = SeqGate()
        gate.parse('lop(xor(opt({f})seq({f}and(opt({a})lop({d})))))')
        all_length_3_routes = gate.get_all_n_length_routes(3)
        self.assertEqual(8, len(all_length_3_routes))

    def test_94(self):
        gate = SeqGate()
        gate.parse('lop(lop(seq(xor({d}{a})and(lop({c}){b})))and(lop({b}){e}))')
        all_length_6_routes = gate.get_all_n_length_routes(6)
        self.assertEqual([], all_length_6_routes)

    def test_95(self):
        gate = SeqGate()
        gate.parse('lop(lop(seq(xor({d}{a})and(lop({c}){b})))and(lop({b}){e}))'
                   'opt(xor(seq({b}{d})lop(opt({f}xor({a}{d})))))')
        all_length_6_routes = gate.get_all_n_length_routes(6)
        self.assertEqual([], all_length_6_routes)

    def test_96(self):
        gate = SeqGate()
        gate.parse('and(and({f}opt(and({f}opt(and({e}{d})))))xor(opt({d})xor({b}xor({c}{a}{b}))))'
                   'lop(xor({a}{c}opt(xor({f}{d}))xor({b}xor({c}{a}{b}))))')
        all_length_8_routes = gate.get_all_n_length_routes(8)
        self.assertEqual(500, len(all_length_8_routes))

    def test_97(self):
        gate = SeqGate()
        gate.parse('xor(and(seq({f}{c})seq({a}{d}{b}))lop({a}))xor(seq(opt({d}){e}lop({g}))seq(xor({a}opt({e})){h})and({h}and({b}{d})))')
        all_length_5_routes = gate.get_all_n_length_routes(5, ('a', 'd', 'b', 'e', 'h'))
        self.assertEqual(500, len(all_length_5_routes))

    def test_legend_1(self):
        gate = SeqGate()
        gate.parse('{a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h})')
        all_length_9_routes = gate.get_all_n_length_routes(9, ('a', 'c', 'd', 'e', 'f', 'd', 'b', 'e', 'h'))
        self.assertEqual(8, len(all_length_9_routes))

    def test_legend_1_2(self):
        gate = SeqGate()
        gate.parse('lop({f}and(xor({b}{c}){d}){e})')
        all_length_4_routes = gate.get_all_n_length_routes(4, ('a', 'c', 'd', 'e', 'f', 'd', 'b', 'e', 'h'))
        self.assertEqual(2, len(all_length_4_routes))

    def test_legend_3_1(self):
        gate = SeqGate()
        gate.parse('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})')
        all_length_5_routes = gate.get_all_n_length_routes(5, ('a', 'c', 'e', 'd', 'h'))
        self.assertEqual(19100, len(all_length_5_routes))

    def test_legend_3_2(self):
        gate = SeqGate()
        gate.parse('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})')
        all_length_11_routes = gate.get_all_n_length_routes(13, ('a', 'c', 'd', 'e', 'f', 'b', 'd', 'e', 'f', 'd', 'b',
                                                                 'e', 'g'))
        # count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
        # for x in all_length_11_routes:
        #     for y in get_event_names(x):
        #         count[y] += 1
        self.assertEqual(19100, len(all_length_11_routes))

    def test_get_min_complexity_1(self):
        gate = SeqGate()
        gate.parse('and(and(seq({h}lop({e}{f}))xor(and(and(seq({a}{g}){d}){g})and(xor({g}{d}){b})))and({e}opt({c})))')

        self.assertEqual(512, gate.get_complexity())

    def test_get_min_complexity_legend(self):
        gate = SeqGate()
        gate.parse('{a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h})')

        self.assertEqual(85 * 8, gate.get_complexity())
        self.assertEqual(5 * 8, gate.get_complexity_for_metric())

    def test_get_min_complexity_legend2(self):
        gate = SeqGate()
        gate.parse('{a}{c}{d}{e}{h}')

        self.assertEqual(1, gate.get_complexity())
        self.assertEqual(1, gate.get_complexity_for_metric())

    def test_get_min_complexity_legend3(self):
        gate = SeqGate()
        gate.parse('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})')


        self.assertEqual(sum(pow(326, i) for i in range(3+1)) * 2, gate.get_complexity())
        self.assertEqual(sum(pow(326, i) for i in range(2+1)) * 2, gate.get_complexity_for_metric())

    def test_get_min_complexity_legend4(self):
        gate = SeqGate()
        gate.parse('xor(seq({a}{c}{d}{e}{h})'
                   'seq({a}{b}{d}{e}{g})'
                    'seq({a}{d}{c}{e}{h})'
                    'seq({a}{b}{d}{e}{h})'
                    'seq({a}{c}{d}{e}{g})'
                    'seq({a}{d}{c}{e}{g})'
                    'seq({a}{d}{b}{e}{h})'
                    'seq({a}{c}{d}{e}{f}{d}{b}{e}{h})'
                    'seq({a}{d}{b}{e}{g})'
                    'seq({a}{c}{d}{e}{f}{b}{d}{e}{h})'
                    'seq({a}{c}{d}{e}{f}{b}{d}{e}{g})'
                    'seq({a}{c}{d}{e}{f}{d}{b}{e}{g})'
                    'seq({a}{d}{c}{e}{f}{c}{d}{e}{h})'
                    'seq({a}{d}{c}{e}{f}{d}{b}{e}{h})'
                    'seq({a}{d}{c}{e}{f}{b}{d}{e}{g})'
                    'seq({a}{c}{d}{e}{f}{b}{d}{e}{f}{d}{b}{e}{g})'
                    'seq({a}{d}{c}{e}{f}{d}{b}{e}{g})'
                    'seq({a}{d}{c}{e}{f}{b}{d}{e}{f}{b}{d}{e}{g})'
                    'seq({a}{d}{c}{e}{f}{d}{b}{e}{f}{b}{d}{e}{h})'
                    'seq({a}{d}{b}{e}{f}{b}{d}{e}{f}{d}{b}{e}{g})'
                    'seq({a}{d}{c}{e}{f}{d}{b}{e}{f}{c}{d}{e}{f}{d}{b}{e}{g}))')

        self.assertEqual(21, gate.get_min_complexity())

    def test_number_of_combos_lop_opt(self):
        # assuming max lop gate length = 3
        gate = SeqGate()
        gate.parse('lop({b})opt({c}{d})lop(xor({e}{b}))')
        all_length_5_routes = gate.get_all_n_length_routes(5)
        # (0,2,3) 2^3 + (1,1,3) 2 * 2^3 + (1,2,2) 2^2 + (2,0,3) 2^3 + (2,1,2) 2 * 2^2 + (2,2,1) 2 +
        # (3,0,2) 2^2 + (3,1,1) 2 * 2 + (3,2,0) 1
        # 8 + 16 + 4 + 8 + 8 + 2 + 4 + 4 + 1
        self.assertEqual(55, len(all_length_5_routes))

    def test_get_next_possible_states(self):
        gate = SeqGate()
        gate.parse('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})')
        events_with_parents = gate.get_events_with_parents()
        e1 = Event('a')
        keys = [x for x in events_with_parents.keys()]
        e2 = keys[1]
        e3 = keys[2]
        e4 = keys[3]

        actual = set(list(events_with_parents[e4].get_next_possible_states((e1, e2, e3), e3, e4)))
        self.assertEqual(7, len(actual))

    def test_get_next_possible_states_2(self):
        gate = SeqGate()
        gate.parse('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})')
        events_with_parents = gate.get_events_with_parents()
        e1 = gate.elements[0]
        keys = [x for x in events_with_parents.keys()]
        e2 = keys[1]

        actual = set(list(events_with_parents[e1].get_next_possible_states((e1, ), e1, e2)))
        self.assertEqual(7, len(actual))

    def test_get_next_possible_states_3(self):
        gate = SeqGate()
        gate.parse('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})')
        e1 = gate.elements[0]

        actual = set(list(gate.get_next_possible_states((), None, e1)))
        self.assertEqual(1, len(actual))

    def test_get_next_possible_states4(self):
        gate = SeqGate()
        gate.parse('{a}and(seq(xor(seq(lop({c})opt({c})){b}){d})lop(seq({f}{d})))xor({e}seq({e}{g}))')
        events_with_parents = gate.get_events_with_parents()
        e1 = Event('a')
        keys = [x for x in events_with_parents.keys()]
        e2 = keys[2]
        e4 = keys[4]
        e8 = keys[8]

        actual = set(list(events_with_parents[e4].get_next_possible_states((e1, e2, e4), e4, e8)))
        self.assertEqual(3, len(actual))

    def test_get_next_possible_states5(self):
        gate = SeqGate()
        gate.parse('{a}and(seq(xor(seq(lop({c})opt({c})){b}){d})lop(seq({f}{d})))xor({e}seq({e}{g}))')
        events_with_parents = gate.get_events_with_parents()
        e1 = Event('a')
        keys = [x for x in events_with_parents.keys()]
        e3 = keys[3]
        e4 = keys[4]
        e8 = keys[8]

        actual = set(list(events_with_parents[e4].get_next_possible_states((e1, e3, e4), e4, e8)))
        self.assertEqual(3, len(actual))


    def test_eq1(self):
        gate1 = SeqGate()
        gate1.parse('and(xor({b}{c}){d}){e})')
        gate2 = SeqGate()
        gate2.parse('and(xor({b}{c}){d}){e})')

        self.assertTrue(gate1 == gate2)

    def test_eq2(self):
        gate1 = SeqGate()
        gate1.parse('and({d}xor({b}{c})){e})')
        gate2 = SeqGate()
        gate2.parse('and(xor({b}{c}){d}){e})')

        self.assertTrue(gate1 == gate2)

    def test_eq3(self):
        gate1 = SeqGate()
        gate1.parse('and(xor({b}{c}){d}){e})')
        gate2 = AndGate()
        gate2.parse('and(xor({b}{c}){d}){e})')

        self.assertFalse(gate1 == gate2)

    def test_eq4(self):
        gate1 = SeqGate()
        gate1.parse('and(xor({b}{c}){d}){e})')
        gate2 = SeqGate()
        gate2.parse('and(opt({b}{c}){d}){e})')

        self.assertFalse(gate1 == gate2)

    def test_eq5(self):
        gate1 = SeqGate()
        gate1.parse('and(xor({b}{c}){d}){e})')
        gate2 = SeqGate()
        gate2.parse('and(xor({e}{c}){d}){e})')

        self.assertFalse(gate1 == gate2)

    def test_count_repeating_if_seq_parent_1(self):
        gate = SeqGate()
        gate.parse('{a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h})')

        self.assertEqual(4, gate.elements[3].count_repeating_if_seq_parent())

    def test_count_repeating_if_seq_parent_2(self):
        gate = SeqGate()
        gate.parse('lop({f}and(xor({b}{c}){d}){e})xor({g}{h})')

        self.assertEqual(0, gate.elements[0].count_repeating_if_seq_parent())

    def test_count_repeating_if_seq_parent_3(self):
        gate = SeqGate()
        gate.parse('{a}{e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h})')

        self.assertEqual(1, gate.elements[2].count_repeating_if_seq_parent())

    def test_count_repeating_if_seq_parent_4(self):
        gate = SeqGate()
        gate.parse('{a}and({d}xor({c}{b})){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h})')

        self.assertEqual(4, gate.elements[3].count_repeating_if_seq_parent())

    def test_count_repeating_if_seq_parent_5(self):
        gate = SeqGate()
        gate.parse('and({a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h}))')

        self.assertEqual(0, gate.elements[0].elements[3].count_repeating_if_seq_parent())


class EventGroupMatcher:
    expected: BaseGroup

    def __init__(self, expected):
        self.expected = expected

    def __eq__(self, other):
        if isinstance(other, EventGroupMatcher):
            other = other.expected
        for event in self.expected.events:
            match = False
            if isinstance(event, Event):
                if isinstance(other, BaseGroup):
                    for other_event in other.events:
                        if isinstance(other_event, Event):
                            if event.name == other_event.name:
                                match = True
                if not match:
                    return False
            else:
                if isinstance(other, BaseGroup):
                    for other_event in other.events:
                        if isinstance(event, BaseGroup):
                            if EventGroupMatcher(event) == other_event:
                                match = True
                if not match:
                    return False
        return True


if __name__ == '__main__':
    unittest.main()
