from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from test.util.test_util import set_params

set_params()
actual = evaluate_guess(
    '{a}and(xor({c}{b}){d}){e}lo3({f}and(xor({c}{b}){d}){e})xor({g}{h}))',
    LogInfo('discovered-processes.csv'), dict(), 6300)
expected = 0
