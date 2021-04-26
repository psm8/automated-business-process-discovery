from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from test.util.test_util import set_params

set_params()
actual = evaluate_guess(
    '{a}{b}{c}osq(opt(lop(opt({d}{e}{f}))seq(lo1({f}{g}{h}{m}){i}))xor({j}{l}{n}{o}{p}){k})',
    LogInfo('v846a16c1050l185.csv'), dict(), 63000)
print(actual)
expected = 0
