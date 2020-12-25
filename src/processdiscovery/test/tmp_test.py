from processdiscovery.evaluation.alignment_calculation import calculate_best_alignment, parallel_event_permutations
from processdiscovery.event.event import Event
from processdiscovery.event.event_group_parallel import EventGroupParallel

event_group = EventGroupParallel([EventGroupParallel([Event('a'), Event('b')]),
                                  Event('c'), Event('d'), Event('e'), Event('f'), Event('g'), Event('h'),
                                  Event('i'), Event('j'), Event('k'), Event('l'), Event('m'), Event('n'),
                                  EventGroupParallel([Event('o'), Event('p'), Event('q')])])

expected = parallel_event_permutations(event_group.events)

# evaluate_guess('and({c}{f})and({b}{f}){a}{d}{a}{e}and({e}{d})')

# e1 = Event('t')
# e2 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
# e3 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
# e4 = EventGroupParallel(string_to_events('xys'))
# e5 = Event('t')
# e6 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
# e7 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
# e8 = EventGroupParallel(string_to_events('xys'))
# e9 = Event('t')
# e10 = EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')])
# e11 = EventGroup([EventGroupParallel(string_to_events('ac')), EventGroup(string_to_events('ez'))])
# e12 = EventGroupParallel(string_to_events('xys'))
# e13 = Event('t')
#
# expected = [[e1, e7, e8, e9, e13], [e1, e10, e13], [e1, e11, e12, e13], [e2, e3, e7, e8, e9],
#             [e2, e3, e10, e13], [e2, e3, e11, e12, e13], [e4, e5, e6, e7, e8, e9, e13],
#             [e4, e5, e6, e10, e13], [e4, e5, e6, e11, e12, e13]]
# expected == flatten_values([[[e1], [e2, e3], [e4, e5, e6]],
#                                            [[e7, e8, e9], [e10], [e11, e12]],
#                                            [[e13]]])