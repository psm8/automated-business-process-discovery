from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo
from processdiscovery.evaluation.alignment_calculation.alignment_calculation import get_best_alignment, parallel_event_permutations
from processdiscovery.event.event import Event
from processdiscovery.event.event_group_parallel import EventGroupParallel

actual = evaluate_guess('lop(seq(lop({g}){a}))lop({f})opt({d})lop({d}){b}lop(opt({h}opt({e}{c})))',
                        LogInfo('discovered-processes.csv'), dict())
expected = 0
