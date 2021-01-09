import unittest

from fitness_functions.process_fitness import evaluate_guess


class MetricsCalculationTest(unittest.TestCase):

    def test_1(self):
        self.assertEqual(1.0, evaluate_guess('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})'))


if __name__ == '__main__':
    unittest.main()
