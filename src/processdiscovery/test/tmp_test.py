from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo

actual = evaluate_guess(
    'opt({b}){a}lop({d}){c}xor({g}seq(opt({d}){e}{h}))opt({f})',
    LogInfo('discovered-processes.csv'), dict(), 2100)
expected = 0