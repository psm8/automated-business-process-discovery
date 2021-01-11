from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from test.util.test_util import set_params

set_params()
actual = evaluate_guess(
    '{a}{c}and({d})and(lo1({f}{d}{b}{e}){e})xor(xor({g}){h})',
    LogInfo('discovered-processes.csv'), dict(), 6300)
expected = 0