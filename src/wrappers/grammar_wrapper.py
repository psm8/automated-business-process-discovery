from representation.grammar import Grammar

from re import match, finditer, DOTALL, MULTILINE
from sys import maxsize

from algorithm import params


class CustomGrammar(Grammar):

    def read_bnf_file(self, file_name):
        """
        Read a grammar file in BNF format. Parses the grammar and saves a
        dict of all production rules and their possible choices.

        :param file_name: A specified BNF grammar file.
        :return: Nothing.
        """

        with open(file_name, 'r') as bnf:
            # Read the whole grammar file.
            content = bnf.read()

            for rule in finditer(self.ruleregex, content, DOTALL):
                # Find all rules in the grammar

                if self.start_rule is None:
                    # Set the first rule found as the start rule.
                    self.start_rule = {"symbol": rule.group('rulename'),
                                       "type": "NT"}

                # Create and add a new rule.
                self.non_terminals[rule.group('rulename')] = {
                    'id': rule.group('rulename'),
                    'min_steps': maxsize,
                    'expanded': False,
                    'recursive': True,
                    'b_factor': 0}

                # Initialise empty list of all production choices for this
                # rule.
                tmp_productions = []

                for p in finditer(self.productionregex,
                                  rule.group('production'), MULTILINE):
                    # Iterate over all production choices for this rule.
                    # Split production choices of a rule.

                    if p.group('production') is None or p.group(
                            'production').isspace():
                        # Skip to the next iteration of the loop if the
                        # current "p" production is None or blank space.
                        continue

                    # Initialise empty data structures for production choice
                    tmp_production, terminalparts = [], None

                    # special cases: GE_RANGE:dataset_n_vars will be
                    # transformed to productions 0 | 1 | ... |
                    # n_vars-1, and similar for dataset_n_is,
                    # dataset_n_os
                    GE_RANGE_regex = r'GE_RANGE:(?P<range>\w*)'
                    m = match(GE_RANGE_regex, p.group('production'))
                    if m:
                        try:
                            if m.group('range') == "dataset_vars":
                                # number of output symbols
                                n = 0
                            elif m.group('range') == "dataset_n_vars":
                                # number of columns from dataset
                                n = params['FITNESS_FUNCTION'].n_vars
                            elif m.group('range') == "dataset_n_is":
                                # number of input symbols (see
                                # if_else_classifier.py)
                                n = params['FITNESS_FUNCTION'].n_is
                            elif m.group('range') == "dataset_n_os":
                                # number of output symbols
                                n = params['FITNESS_FUNCTION'].n_os
                            else:
                                # assume it's just an int
                                n = int(m.group('range'))
                        except (ValueError, AttributeError):
                            raise ValueError("Bad use of GE_RANGE: "
                                             + m.group())

                        if n > 0 :
                            for i in range(n):
                                # add a terminal symbol
                                tmp_production, terminalparts = [], None
                                symbol = {
                                    "symbol": str(i),
                                    "type": "T",
                                    "min_steps": 0,
                                    "recursive": False}
                                tmp_production.append(symbol)
                                if str(i) not in self.terminals:
                                    self.terminals[str(i)] = \
                                        [rule.group('rulename')]
                                elif rule.group('rulename') not in \
                                    self.terminals[str(i)]:
                                    self.terminals[str(i)].append(
                                        rule.group('rulename'))
                                tmp_productions.append({"choice": tmp_production,
                                                        "recursive": False,
                                                        "NT_kids": False})
                            # don't try to process this production further
                            # (but later productions in same rule will work)
                            continue
                        else:
                            for var in params['FITNESS_FUNCTION'].vars:
                                # add a terminal symbol
                                tmp_production, terminalparts = [], None
                                symbol = {
                                    "symbol": var,
                                    "type": "T",
                                    "min_steps": 0,
                                    "recursive": False}
                                tmp_production.append(symbol)
                                if var not in self.terminals:
                                    self.terminals[var] = \
                                        [rule.group('rulename')]
                                elif rule.group('rulename') not in \
                                        self.terminals[var]:
                                    self.terminals[var].append(
                                        rule.group('rulename'))
                                tmp_productions.append({"choice": tmp_production,
                                                        "recursive": False,
                                                        "NT_kids": False})
                            # don't try to process this production further
                            # (but later productions in same rule will work)
                            continue

                    for sub_p in finditer(self.productionpartsregex,
                                          p.group('production').strip()):
                        # Split production into terminal and non terminal
                        # symbols.

                        if sub_p.group('subrule'):
                            if terminalparts is not None:
                                # Terminal symbol is to be appended to the
                                # terminals dictionary.
                                symbol = {"symbol": terminalparts,
                                          "type": "T",
                                          "min_steps": 0,
                                          "recursive": False}
                                tmp_production.append(symbol)
                                if terminalparts not in self.terminals:
                                    self.terminals[terminalparts] = \
                                        [rule.group('rulename')]
                                elif rule.group('rulename') not in \
                                    self.terminals[terminalparts]:
                                    self.terminals[terminalparts].append(
                                        rule.group('rulename'))
                                terminalparts = None

                            tmp_production.append(
                                {"symbol": sub_p.group('subrule'),
                                 "type": "NT"})

                        else:
                            # Unescape special characters (\n, \t etc.)
                            if terminalparts is None:
                                terminalparts = ''
                            terminalparts += ''.join(
                                [part.encode().decode('unicode-escape') for
                                 part in sub_p.groups() if part])

                    if terminalparts is not None:
                        # Terminal symbol is to be appended to the terminals
                        # dictionary.
                        symbol = {"symbol": terminalparts,
                                  "type": "T",
                                  "min_steps": 0,
                                  "recursive": False}
                        tmp_production.append(symbol)
                        if terminalparts not in self.terminals:
                            self.terminals[terminalparts] = \
                                [rule.group('rulename')]
                        elif rule.group('rulename') not in \
                            self.terminals[terminalparts]:
                            self.terminals[terminalparts].append(
                                rule.group('rulename'))
                    tmp_productions.append({"choice": tmp_production,
                                            "recursive": False,
                                            "NT_kids": False})

                if not rule.group('rulename') in self.rules:
                    # Add new production rule to the rules dictionary if not
                    # already there.
                    self.rules[rule.group('rulename')] = {
                        "choices": tmp_productions,
                        "no_choices": len(tmp_productions)}

                    if len(tmp_productions) == 1:
                        # Unit productions.
                        print("Warning: Grammar contains unit production "
                              "for production rule", rule.group('rulename'))
                        print("         Unit productions consume GE codons.")
                else:
                    # Conflicting rules with the same name.
                    raise ValueError("lhs should be unique",
                                     rule.group('rulename'))