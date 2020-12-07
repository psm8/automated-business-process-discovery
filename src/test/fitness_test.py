from fitness.process_fitness import evaluate_guess

evaluate_guess('and({a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n})')
evaluate_guess('{f}xor({d}and({b}lop({b})opt({a})))')
evaluate_guess('lop(opt(seq(xor({e}{c})lop({d}))){f})')
evaluate_guess('and(lop(opt(seq(xor({e}{c})lop({d}))){f}){a})and({d}{a})')
evaluate_guess('lop(xor({b}xor({a}{e}{d})){e})')
