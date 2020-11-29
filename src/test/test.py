from fitness.process_fitness import evaluate_guess

evaluate_guess('lop(opt(seq(xor({e}{c})lop({d}))){f})')
evaluate_guess('and(lop(opt(seq(xor({e}{c})lop({d}))){f}){a})and({d}{a})')
evaluate_guess('lop(xor({b}xor({a}{e}{d})){e})')
