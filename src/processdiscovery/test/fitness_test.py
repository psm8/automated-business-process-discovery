import unittest

from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo


class FitnessTest(unittest.TestCase):

    def test_1(self):
        self.assertEqual(1.0, evaluate_guess('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})'))

    def test_2(self):
        evaluate_guess('{f}xor({d}and({b}lop({b})opt({a})))')

    def test_3(self):
        evaluate_guess('lop(opt(seq(xor({e}{c})lop({d}))){f})')

    def test_4(self):
        evaluate_guess('and(lop(opt(seq(xor({e}{c})lop({d}))){f}){a})and({d}{a})')

    def test_5(self):
        evaluate_guess('lop(xor({b}xor({a}{e}{d})){e})')

    def test_6(self):
        evaluate_guess('xor(and({c}and(and({c}{b}and({d}{f})){b}{e})){e}{e})')

    def test_7(self):
        # 'and({d}{d})lop({b})'
        evaluate_guess('lop({c})')

    def test_8(self):
        evaluate_guess('and({a}{f}opt(and({b}{e}lop({c}))){d})')

    def test_legend(self):

        actual = evaluate_guess('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})', LogInfo('discovered-processes.csv'),
                                dict())

        self.assertEqual(0.8, actual)

if __name__ == '__main__':
    unittest.main()
