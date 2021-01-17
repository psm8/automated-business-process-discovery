from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from test.util.test_util import set_params

set_params()
actual = evaluate_guess(
    '{a}lo1({f}xor(opt({c}){b}){d}{e}xor({h}{g}))',
    LogInfo('discovered-processes.csv'), dict(), 6300)
expected = 0
