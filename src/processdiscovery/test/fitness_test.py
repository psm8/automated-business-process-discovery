import unittest

from fitness.process_fitness import evaluate_guess


class AlignmentCalculationTest(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
