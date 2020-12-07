import unittest

from gate.seq_gate import SeqGate
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel
from test.test_util import string_to_events

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


if __name__ == '__main__':
    unittest.main()
