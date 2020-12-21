import unittest

from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.event.event import Event
from processdiscovery.event.base_group import BaseGroup
from processdiscovery.event.event_group import EventGroup
from processdiscovery.event.event_group_parallel import EventGroupParallel
from processdiscovery.test import string_to_events
from processdiscovery.util.util import to_n_length, to_n_length_opt


class GateTest(unittest.TestCase):

    def test_1(self):
        gate = SeqGate()
        gate.parse('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})')
        self.assertCountEqual([EventGroupMatcher(EventGroup([EventGroupParallel(string_to_events('abcdefghijklmn'))]))],
                              gate.get_all_n_length_routes(14))
        self.assertEqual([], gate.get_all_n_length_routes(13))

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
        self.assertEqual([EventGroupMatcher(EventGroup([EventGroupParallel(string_to_events('cccccc'))]))], gate.get_all_n_length_routes(6))

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
        gate.parse('lop({b})opt({c}{d})lop(xor({e}{b}))')
        all_length_5_routes = gate.get_all_n_length_routes(5)
        #  (0,0,5) 2^5 + (0,1,4) 2 * 2^4 + (0,2,3) 2^3 + (1,0,4) 2^4 + (1,1,3) 2 * 2^3 + (1,2,2) 2^2 + (2,0,3) 2^3
        # (2^6 + 2^3) + (2^5 + 2^2) + (2^4 + 2)  + (2^3  +1) + (2^2) + 1  = 2^7 + 2^3 + 2^2 = 140
        self.assertEqual(10, len(all_length_5_routes))

    def test_to_n_length(self):
        e1 = Event('t')
        e2 = EventGroupParallel([EventGroupParallel(string_to_events('t')), Event('q')])
        e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e4 = EventGroupParallel(string_to_events('xys'))

        expected = [EventGroupParallel([e1, e1, e1, e1]), EventGroupParallel([e1, e1, e2]),
                    EventGroupParallel([e1, e4]), EventGroupParallel([e2, e2]), e3]
        self.assertEqual(len(expected), len(to_n_length(4, [e1, e2, e3, e4])))

    def test_to_n_length_opt(self):
        e1 = Event('t')
        e2 = EventGroupParallel([EventGroupParallel(string_to_events('t')), Event('q')])
        e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
        e4 = EventGroupParallel(string_to_events('xys'))

        expected = [EventGroupParallel([e1, e4]), e3]
        self.assertEqual(len(expected), len(to_n_length_opt(4, [e1, e2, e3, e4])))

    def test_to_n_length_opt2(self):
        e1 = Event('e')
        e2 = EventGroup([Event('f'), Event('f'), Event('f')])
        e3 = EventGroup([Event('f'), Event('f'), Event('f'), Event('f')])

        expected = [EventGroupParallel([e1, e2]), e3]
        self.assertEqual(len(expected), len(to_n_length_opt(4, [e1, e2, e3])))


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
