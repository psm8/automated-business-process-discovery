import unittest

from fitness.alignment_calculation import *
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel


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
        event_group_events = []
        for x in 'pqacezxys':
            event_group_events.append(Event(x))
        event_group = EventGroup(event_group_events)

        # self.assertEqual(nw_wrapper('zxabcdezx', event_group), -8)
        nw_wrapper('zxabcdezx', event_group)


    def test_fill_result_matrix(self):
        matrix = [[0, -1, -2], [-1, 0, -1], [-2, -1, 0]]

    def test_resolve_parallel(self):


if __name__ == '__main__':
    unittest.main()
