import unittest

from process_discovery.evaluation.metrics_calculation import evaluate_guess
from process_discovery.log.log_util import LogInfo
from test.util.test_util import set_params


class FitnessTest(unittest.TestCase):

    def test_1(self):
        set_params()
        self.assertEqual(1.0, evaluate_guess('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})',
                                             LogInfo('v21a81391l17.csv'), dict(), 2100000000000000000))

    def test_no_exceptions_2(self):
        set_params()
        evaluate_guess('{f}xor({d}and({b}lop({b})opt({a})))', LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_no_exceptions_3(self):
        set_params()
        evaluate_guess('lop(opt(seq(xor({e}{c})lop({d}))){f})', LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_no_exceptions_4(self):
        set_params()
        evaluate_guess('and(lop(opt(seq(xor({e}{c})lop({d}))){f}){a})and({d}{a})', LogInfo('v21a81391l17.csv'),
                       dict(), 2100)

    def test_no_exceptions_5(self):
        set_params()
        evaluate_guess('lop(xor({b}xor({a}{e}{d})){e})', LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_no_exceptions_6(self):
        set_params()
        evaluate_guess('xor(and({c}and(and({c}{b}and({d}{f})){b}{e})){e}{e})', LogInfo('v21a81391l17.csv'),
                       dict(), 2100)

    def test_no_exceptions_7(self):
        set_params()
        evaluate_guess('lop({c})', LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_no_exceptions_8(self):
        set_params()
        evaluate_guess('and({a}{f}opt(and({b}{e}lop({c}))){d})', LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_no_exceptions_9(self):
        set_params()
        evaluate_guess('and(xor({a}{f}{g}and({b}and(and({d}{c}){e}{f})))opt({d}))'
                       'and(xor(opt({f}{h})and(and({d}{g})and({b}opt({e})))){h})',
                        LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_9_1(self):
        set_params()
        actual = evaluate_guess('lop(seq(lop({g}){a}))lop({f})opt({d})lop({d}){b}lop(opt({h}opt({e}{c})))',
                                LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_9_2(self):
        actual = evaluate_guess('xor(opt({f})and(and({h}and({d}{c}{e}))opt({b}){a})'
                                'and(opt(and({h}and({b}{c}{a})){g}){a}))',
                                LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_9_3(self):
        set_params()
        actual = evaluate_guess(
            'and(xor({b}seq(opt({h})opt({c})opt({f})){c}){e}seq(opt({h}){a}{b}{d}))opt({g})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_4(self):
        set_params()
        actual = evaluate_guess(
            'and(xor({b}seq(opt({h})opt({c})opt({f})){c}){e}seq(opt({h}){a}{b}{d}))opt({g})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_5(self):
        set_params()
        actual = evaluate_guess(
            'and({a}and(and(opt({b})opt(seq(opt({f}){g})))lop(and({c}{d}){e})))opt({h})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_6(self):
        set_params()
        actual = evaluate_guess(
            'and(lop({c}{d}){a})and({h}seq(and(opt({f}{d}{b})opt({c}))opt({g}){e}))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_7(self):
        set_params()
        actual = evaluate_guess(
            '{a}and(and(opt({e})seq(xor({d}{e}){b}))xor(opt({g})xor(xor({h}xor({f}{h}))xor({f}and(and({c}{h}){a})))))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_8(self):
        set_params()
        actual = evaluate_guess(
            '{a}{c}opt(seq(and({f}{b}){e}))opt(seq(and({f}{b}){e})){d}xor(opt({g})and({e}{h}))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9(self):
        set_params()
        actual = evaluate_guess(
            '{a}and(seq(xor(seq(lop({c})opt({c})){b}){d})lop(seq({f}{d})))'
            'xor({e}seq({e}{g}))xor({h}seq({c}and({c}{h})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_1(self):
        set_params()
        actual = evaluate_guess(
            'xor(and(seq({f}{c})seq({a}{d}{b}))lop({a}))xor(seq(opt({d}){e}lop({g}))seq(xor({a}opt({e})){h})and({h}and({b}{d})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_2(self):
        set_params()
        actual = evaluate_guess(
            '{a}{d}{c}opt(and(xor({f}and(and({b}{g})lop({a}))and(lop({g}){e}))lop({h})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_3(self):
        set_params()
        actual = evaluate_guess(
            '{a}and(xor(seq({b}opt({d}{f})){c})opt({d}))xor(seq(opt({e}){h})opt(seq({e}{g})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_4(self):
        set_params()
        actual = evaluate_guess(
            'and({d}{a})and(and(seq({e}lop({c}))opt({e}{g}))xor({c}{h}seq(lop({e})opt({f}){b})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_5(self):
        set_params()
        actual = evaluate_guess(
            'and(seq({c}{d}{e}{a})opt(seq({c}{d}lop(seq({f}{d})))))lop(xor({g}{b}{h}))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_6(self):
        set_params()
        actual = evaluate_guess(
            '{h}{d}{g}{c}xor(opt({e}){f})xor({a}and(lop(seq(opt({c})opt({b})))opt({d})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_7(self):
        set_params()
        actual = evaluate_guess(
            '{a}xor(and({g}and({e}{f}))xor(and({g}and({e}{c}))and(seq(xor({f}{h}){d}{b}){h})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_8(self):
        set_params()
        actual = evaluate_guess(
            '{a}{c}{d}and(seq(xor(opt({c})seq({b}{e}){e}xor(xor({f}{h}){g})){e})opt(lop({a})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9(self):
        set_params()
        actual = evaluate_guess(
            'and(xor({c}{e}xor({e}xor({a}{b}){a}))and({a}and({d}{c})))xor({h}{g}{f})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_0(self):
        set_params()
        actual = evaluate_guess(
            'xor(seq({a}and(xor({c}{b}){d}){e}lop(and(xor({c}{b}){d}))xor({g}{h})){f})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_1(self):
        actual = evaluate_guess(
            '{a}xor(and(and(xor(and({b}{e})and({b}and({b}{f})))and({h}and({a}{c}))){g})seq({h}and({f}{d}){c}))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_2(self):
        set_params()
        actual = evaluate_guess(
            'lo0(xor(and({e}seq({d}{b}{c}))seq({f}{g}{d}{h}{a}and({f}{e}))))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_3(self):
        set_params()
        actual = evaluate_guess(
            '{a}xor(and({d}{c})xor({b}{e}))and(lop({g})xor(seq(lo0({c}xor({d}{f})){e})and({e}{h})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_4(self):
        set_params()
        actual = evaluate_guess(
            'and(xor({d}{a})and({d}{c}))xor(lop({g})seq({e}{f}{d}{b}))and(opt({h}){e})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_5(self):
        set_params()
        actual = evaluate_guess(
            'xor({f}{a})xor({e}seq({g}opt({b}){h})and(opt({e})seq({b}{d})))'
            'xor(seq({h}opt(xor(seq({f}{g})seq({h}{c}{d}))))'
            'seq(xor(seq({b}{d}){e}opt({d}))xor(and(lop({e}{d}){e}){g})))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_6(self):
        set_params()
        actual = evaluate_guess(
            'and(xor(opt(lop({f}))xor(and({e}{a}seq({c}{d})opt({g}))and({b}{h}){g})'
            'xor(xor(and({e}{a}seq({c}{d}))opt({b}))xor(xor(opt({c})lop({c}))seq({b}{d}))))opt({h}))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_7(self):
        set_params()
        actual = evaluate_guess(
            'xor(and(seq(xor({c}xor(seq({b}{d}){c}))xor({f}{e}))xor({a}{b}))'
            'seq(xor({h}xor({e}and({d}{a})))xor({a}opt({c}))))opt(xor({g}{h}{c}{f}))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_8(self):
        set_params()
        actual = evaluate_guess(
            'and(seq({a}seq(xor({f}opt(lo1({c})))))seq(lo1({f}{b}{d}{e})))xor({g}{h})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9(self):
        set_params()
        actual = evaluate_guess(
            '{a}{c}and({d})and(lo1({f}{d}{b}{e}){e})xor(xor({g}){h})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_0(self):
        set_params()
        actual = evaluate_guess(
            'seq(and(xor({a}))xor({c}))xor(xor({f})xor({b}{d}))seq(and({e}lo0(and({g}))))opt(and({h}))',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_1(self):
        set_params()
        actual = evaluate_guess(
            '{a}xor({c}{b}{h})and(opt(and({g})){d}{e})lo1({h})',
            LogInfo('v21a81391l17.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_2(self):
        set_params()
        actual = evaluate_guess(
            '{a}seq({b}and(opt(seq({d}){e})){h})xor({g}and(opt({a}))opt(opt(and({d}))xor(seq({c}){e}seq({e}){a})))',
            LogInfo('v8a7c1254l5.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_3(self):
        set_params()
        actual = evaluate_guess(
            '{a}xor(xor(xor({b})lo2({b}){b}){c}seq(and(and({b})){e})){d}opt(xor(and({e}opt(xor({h}{g})))){h}',
            LogInfo('v8a7c1254l5.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_4(self):
        set_params()
        actual = evaluate_guess(
            '{a}opt(seq(and(and({e})opt({c}))){d}){h}xor(seq(xor(and({e}{c}){c}))seq(opt(xor(and({a}))lo2({g})))xor(xor({d}{g}and({e}))opt({b}){g}{c}opt({b})opt({e}{d}){h}))',
            LogInfo('v8a7c1254l5.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_5(self):
        set_params()
        actual = evaluate_guess(
            '{a}and({d})xor({b})xor(xor(opt(seq(seq({a}xor({a}seq({h}))and({h}{f})){h}))){h}{a}seq(opt({h})xor({c})and(and({h})opt({h}))){g}and(xor(lo2(and(and({g})))){e}))opt({h})',
            LogInfo('v8a7c1254l5.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_6(self):
        set_params()
        actual = evaluate_guess(
            'seq({a})xor({b}{f}{c}){d}and(xor({h}xor(and(xor(and({c})))lo0(xor({b}{f}{d}{g})))){e})opt({h})',
            LogInfo('v8a7c1254l5.csv'), dict(), 2100)
        expected = 0

    def test_9_9_9_9_7(self):
        set_params()
        actual = evaluate_guess('{a}lo0(and({c}{b}))opt(seq({e}{f}))lo4(and({c}{b})){d}',
                                LogInfo('v6a6c13l12.csv'),
                                dict(), 2100000000000)

    def test_9_9_9_9_8(self):
        set_params()
        actual = evaluate_guess('{a}lo3(lo3(opt({d}))and({d}))opt({c}{b}){e}',
                                LogInfo('v8a5c40l5.csv'),
                                dict(), 2100000000000)

    def test_legend_1_0_1(self):
        set_params()
        actual = evaluate_guess('{a}lo1({f}and(xor({b}{c}){d}){e})xor({g}{h})',
                                LogInfo('v21a81391l17.csv'), dict(), 2100)
        self.assertTrue(actual > 0.985)

    def test_legend_1_0_2(self):
        set_params()
        actual1 = evaluate_guess('{a}lo1({f}and(xor({b}{c}){d}){e})xor({g}{h})',
                                LogInfo('v21a81391l17.csv'), dict(), 6300)
        actual2 = evaluate_guess('{a}lo1({f}and(xor({b}{c}){d}){e})opt({h})opt({g})',
                                LogInfo('v21a81391l17.csv'), dict(), 6300)
        self.assertTrue(actual1 > actual2)

    def test_legend_1_1(self):
        set_params()
        actual = evaluate_guess('{a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h})',
                                LogInfo('v21a81391l17.csv'), dict(), 2100)
        self.assertTrue(actual > 0.985)

    def test_legend_1_2(self):
        set_params()
        actual = evaluate_guess('{a}and(xor({b}{c}){d}){e}opt(seq({f}and(xor({b}{c}){d}){e}))xor({g}{h})',
                                LogInfo('v21a81391l17.csv'), dict(), 21000000)

    def test_legend_1_3(self):
        set_params()
        actual = evaluate_guess('{a}lop(and(xor({b}{c}){d}){e}xor({f}))xor({g}{h})',
                                LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_legend_1_4(self):
        set_params()
        actual = evaluate_guess('{a}and(xor({b}{c}){d}){e}opt({f})xor({g}{h})',
                                LogInfo('v21a81391l17.csv'), dict(), 2100)

    def test_legend_1_5(self):
        set_params()
        actual = evaluate_guess('and({a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h}))',
                                LogInfo('v21a81391l17.csv'), dict(), 2100000)

    def test_legend_1_6(self):
        set_params()
        actual = evaluate_guess('opt({a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h}))',
                                LogInfo('v21a81391l17.csv'), dict(), 2100000)

    def test_legend_1_7(self):
        set_params()
        actual = evaluate_guess('xor({a}and(xor({b}{c}){d}){e}lop({f}and(xor({b}{c}){d}){e})xor({g}{h}))',
                                LogInfo('v21a81391l17.csv'), dict(), 2100000)

    def test_legend2(self):
        set_params()
        actual = evaluate_guess('{a}{c}{d}{e}{h}', LogInfo('v21a81391l17.csv'),
                                dict(), 2100)

    def test_legend3(self):
        set_params()
        actual = evaluate_guess('{a}lop(opt({b}{c}{d}{e}{f}))xor({g}{h})', LogInfo('v21a81391l17.csv'),
                                dict(), 2100000000000)

    def test_legend4(self):
        set_params()
        actual = evaluate_guess('xor(seq({a}{c}{d}{e}{h})'
                                'seq({a}{b}{d}{e}{g})'
                                'seq({a}{d}{c}{e}{h})'
                                'seq({a}{b}{d}{e}{h})'
                                'seq({a}{c}{d}{e}{g})'
                                'seq({a}{d}{c}{e}{g})'
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
                                'seq({a}{d}{c}{e}{f}{d}{b}{e}{f}{b}{d}{e}{h})'
                                'seq({a}{d}{b}{e}{f}{b}{d}{e}{f}{d}{b}{e}{g})'
                                'seq({a}{d}{c}{e}{f}{d}{b}{e}{f}{c}{d}{e}{f}{d}{b}{e}{g}))',
                                LogInfo('v21a81391l17.csv'), dict(), 2100)


if __name__ == '__main__':
    unittest.main()
