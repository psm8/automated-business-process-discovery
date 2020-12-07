from gate.seq_gate import SeqGate
from fitness.process_fitness import evaluate_guess
from fitness.alignment_calculation import *
from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel

gate = SeqGate()
gate.parse('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})')

'xor({e}seq(and({c}{f}){b}and({d}{f})and({a}{e})))'
test = gate.get_all_n_length_routes(14)

print(test)

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