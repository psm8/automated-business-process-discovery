from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from test.util.test_util import set_params

set_params()
actual = evaluate_guess(
    '{a}xor(seq({b}{d})seq({c}{d})seq({d}xor({b}{c}))){e}xor({h}{g})',
    LogInfo('v8a7c1254l5.csv'), dict(), 6300)
expected = 0
