from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo

actual = evaluate_guess(
    '{h}{d}{g}{c}xor(opt({e}){f})xor({a}and(lop(seq(opt({c})opt({b})))opt({d})))',
    LogInfo('discovered-processes.csv'), dict(), 2100)
expected = 0