import unittest

from gate.seq_gate import SeqGate
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel
from test.test_util import string_to_events
from util.util import to_n_length, to_n_length_opt, flatten_values


class GateTest(unittest.TestCase):

    def test_1(self):
        gate = SeqGate()
        gate.parse('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})')
        self.assertEqual([EventGroup([EventGroupParallel(string_to_events('abcdefghijklmn'))])], gate.get_all_n_length_routes(14))
        self.assertEqual([], gate.get_all_n_length_routes(13))

    def test_2(self):
        gate = SeqGate('{f}xor({d}and({b}lop({b})opt({a})))')

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
        self.assertEqual([EventGroup([EventGroupParallel(string_to_events('abcdefghijklmn'))])], gate.get_all_n_length_routes(6))

    def test_8(self):
        gate = SeqGate()
        gate.parse('xor({f}{d}and({e}xor(lop(xor({f}{d}))lop({a}))))and({b}{a})')
        all_n_routes = gate.get_all_n_length_routes(3)
        self.assertEqual([EventGroup([EventGroupParallel(string_to_events('abcdefghijklmn'))])], all_n_routes)

    def test_9(self):
        gate = SeqGate()
        gate.parse('and({c}and({a}lop({a}opt({d}))seq({c}{b})))')
        all_n_routes = gate.get_all_n_length_routes(5)
        self.assertEqual([EventGroup([EventGroupParallel(string_to_events('abcdefghijklmn'))])], all_n_routes)

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
