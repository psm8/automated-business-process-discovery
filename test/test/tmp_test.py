from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from test.util.test_util import set_params

set_params()
actual = evaluate_guess(
    '{a}opt({c})lo1({f}opt({b}){d}{e})opt({g})opt({h})',
    LogInfo('discovered-processes.csv'), dict(), 6300)
expected = 0
