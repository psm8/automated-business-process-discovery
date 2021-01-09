from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo

actual = evaluate_guess(
    'seq({a}xor(and({d}{c})seq({b}xor({d}{g})))){e}{h}opt(seq({f}{d}lo2({f}{d})))',
    LogInfo('discovered-processes.csv'), dict(), 2100)
expected = 0