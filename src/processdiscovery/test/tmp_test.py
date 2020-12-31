from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo


actual = evaluate_guess('xor(opt({f})and(and({h}and({d}{c}{e}))opt({b}){a})and(opt(and({h}and({b}{c}{a})){g}){a}))',
                        LogInfo('discovered-processes.csv'), dict(), 21000)
expected = 0
