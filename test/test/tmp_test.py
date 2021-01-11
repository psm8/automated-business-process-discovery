from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from algorithm.parameters import params

params['RESULT_TOLERANCE_PERCENT'] = 5
params['WEIGHT_ALIGNMENT'] = 6
params['WEIGHT_COMPLEXITY'] = 2
params['WEIGHT_GENERALIZATION'] = 2
params['WEIGHT_PRECISION'] = 2
params['WEIGHT_SIMPLICITY'] = 2
params['MINIMIZE_SOLUTION_LENGTH'] = True
actual = evaluate_guess(
    '{a}lo1({f}and(xor({b}{c}){d}){e})opt({h})xor(seq(and(seq(lo1({g})))))',
    LogInfo('discovered-processes.csv'), dict(), 2100)
expected = 0