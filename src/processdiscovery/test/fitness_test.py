import unittest

from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo


class FitnessTest(unittest.TestCase):

    def test_1(self):
        self.assertEqual(1.0, evaluate_guess('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})',
                                             LogInfo('discovered-processes.csv'), dict()))

    def test_2(self):
        evaluate_guess('{f}xor({d}and({b}lop({b})opt({a})))', LogInfo('discovered-processes.csv'), dict())

    def test_3(self):
        evaluate_guess('lop(opt(seq(xor({e}{c})lop({d}))){f})', LogInfo('discovered-processes.csv'), dict())

    def test_4(self):
        evaluate_guess('and(lop(opt(seq(xor({e}{c})lop({d}))){f}){a})and({d}{a})', LogInfo('discovered-processes.csv'),
                       dict())

    def test_5(self):
        evaluate_guess('lop(xor({b}xor({a}{e}{d})){e})', LogInfo('discovered-processes.csv'), dict())

    def test_6(self):
        evaluate_guess('xor(and({c}and(and({c}{b}and({d}{f})){b}{e})){e}{e})', LogInfo('discovered-processes.csv'),
                       dict())

    def test_7(self):
        # 'and({d}{d})lop({b})'
        evaluate_guess('lop({c})', LogInfo('discovered-processes.csv'), dict())

    def test_8(self):
        evaluate_guess('and({a}{f}opt(and({b}{e}lop({c}))){d})', LogInfo('discovered-processes.csv'), dict())

    def test_legend(self):

        actual = evaluate_guess('{a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h})',
                                LogInfo('discovered-processes.csv'), dict())

        self.assertEqual(0.8, actual)

    def test_legend2(self):

        actual = evaluate_guess('{a}{c}{d}{e}{h}', LogInfo('discovered-processes.csv'),
                                dict())

        self.assertEqual(0.8, actual)

    def test_legend3(self):

        actual = evaluate_guess('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})', LogInfo('discovered-processes.csv'),
                                dict())

        self.assertEqual(0.8, actual)

    def test_legend4(self):

        actual = evaluate_guess('xor(seq({a}{c}{e}{d}{h})'
                                'seq({a}{b}{d}{e}{g})'
                                'seq({a}{d}{c}{e}{h})'
                                'seq({a}{d}{c}{e}{h})'
                                'seq({a}{b}{d}{e}{h})'
                                'seq({a}{c}{d}{e}{g})'
                                'seq({a}{d}{b}{e}{h})'
                                'seq({a}{c}{d}{e}{f}{d}{b}{e}{h})'
                                'seq({a}{d}{b}{e}{g})'
                                'seq({a}{c}{d}{e}{f}{b}{d}{e}{h})'
                                'seq({a}{c}{d}{e}{f}{b}{d}{e}{g})'
                                'seq({a}{c}{d}{e}{f}{d}{b}{e}{g})'
                                'seq({a}{d}{c}{e}{f}{c}{d}{e}{h})'
                                'seq({a}{d}{c}{e}{f}{d}{b}{e}{h})'
                                'seq({a}{d}{c}{e}{f}{b}{d}{e}{g})'
                                'seq({a}{c}{d}{e}{f}{b}{d}{e}{f}{d}{b}{e}{g})'
                                'seq({a}{d}{c}{e}{f}{d}{b}{e}{g})'
                                'seq({a}{d}{c}{e}{f}{b}{d}{e}{f}{b}{d}{e}{g})'
                                'seq({a}{d}{c}{e}{f}{d}{b}{e}{f}{b}{d}{e}{h })'
                                'seq({a}{d}{b}{e}{f}{b}{d}{e}{f}{d}{b}{e}{g})'
                                'seq({a}{d}{c}{e}{f}{d}{b}{e}{f}{c}{d}{e}{f}{d}{b}{e}{g}))',
                                LogInfo('discovered-processes.csv'), dict())

        self.assertEqual(0.8, actual)


if __name__ == '__main__':
    unittest.main()
