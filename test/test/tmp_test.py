from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo

actual = evaluate_guess(
    '{a}lo1({f}{c}{d})opt({b}){e}xor({g}{h})',
    LogInfo('discovered-processes.csv'), dict(), 2100)
expected = 0