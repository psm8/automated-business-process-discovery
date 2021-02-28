from os import path
from socket import gethostname

hostname = gethostname().split('.')
machine_name = hostname[0]

import importlib
from algorithm.parameters import params, load_params
from wrappers.grammar_wrapper import CustomGrammar
from utilities.algorithm.initialise_run import return_attr_from_module, get_fit_func_imports


def set_params(command_line_args, create_files=True):
    """
    This function parses all command line arguments specified by the user.
    If certain parameters are not set then defaults are used (e.g. random
    seeds, elite size). Sets the correct imports given command line
    arguments. Sets correct grammar file and fitness function. Also
    initialises save folders and tracker lists in utilities.trackers.

    :param command_line_args: Command line arguments specified by the user.
    :return: Nothing.
    """

    from utilities.algorithm.initialise_run import initialise_run_params
    from utilities.fitness.math_functions import return_one_percent
    from utilities.algorithm.command_line_parser import parse_cmd_args
    from utilities.stats import trackers
    from utilities.stats import clean_stats

    cmd_args, unknown = parse_cmd_args(command_line_args)

    if unknown:
        # We currently do not parse unknown parameters. Raise error.
        s = "algorithm.parameters.set_params\nError: " \
            "unknown parameters: %s\nYou may wish to check the spelling, " \
            "add code to recognise this parameter, or use " \
            "--extra_parameters" % str(unknown)
        raise Exception(s)

    # LOAD PARAMETERS FILE
    # NOTE that the parameters file overwrites all previously set parameters.
    if 'PARAMETERS' in cmd_args:
        load_params(path.join("..", "parameters", cmd_args['PARAMETERS']))

    # Join original params dictionary with command line specified arguments.
    # NOTE that command line arguments overwrite all previously set parameters.
    params.update(cmd_args)

    if params['LOAD_STATE']:
        # Load run from state.
        from utilities.algorithm.state import load_state

        # Load in state information.
        individuals = load_state(params['LOAD_STATE'])

        # Set correct search loop.
        from algorithm.search_loop import search_loop_from_state
        params['SEARCH_LOOP'] = search_loop_from_state

        # Set population.
        setattr(trackers, "state_individuals", individuals)

    else:
        if params['REPLACEMENT'].split(".")[-1] == "steady_state":
            # Set steady state step and replacement.
            params['STEP'] = "steady_state_step"
            params['GENERATION_SIZE'] = 2

        else:
            # Elite size is set to either 1 or 1% of the population size,
            # whichever is bigger if no elite size is previously set.
            if params['ELITE_SIZE'] is None:
                params['ELITE_SIZE'] = return_one_percent(1, params[
                    'POPULATION_SIZE'])

            # Set the size of a generation
            params['GENERATION_SIZE'] = params['POPULATION_SIZE'] - \
                                        params['ELITE_SIZE']

        # Initialise run lists and folders before we set imports.r
        initialise_run_params(create_files)

        # Set correct param imports for specified function options, including
        # error metrics and fitness functions.
        set_param_imports()

        # Clean the stats dict to remove unused stats.
        clean_stats.clean_stats()

        # Set GENOME_OPERATIONS automatically for faster linear operations.
        if (params['CROSSOVER'].representation == "subtree" or
                params['MUTATION'].representation == "subtree"):
            params['GENOME_OPERATIONS'] = False
        else:
            params['GENOME_OPERATIONS'] = True

        # Ensure correct operators are used if multiple fitness functions used.
        if hasattr(params['FITNESS_FUNCTION'], 'multi_objective'):

            # Check that multi-objective compatible selection is specified.
            if not hasattr(params['SELECTION'], "multi_objective"):
                s = "algorithm.parameters.set_params\n" \
                    "Error: multi-objective compatible selection " \
                    "operator not specified for use with multiple " \
                    "fitness functions."
                raise Exception(s)

            if not hasattr(params['REPLACEMENT'], "multi_objective"):

                # Check that multi-objective compatible replacement is
                # specified.
                if not hasattr(params['REPLACEMENT'], "multi_objective"):
                    s = "algorithm.parameters.set_params\n" \
                        "Error: multi-objective compatible replacement " \
                        "operator not specified for use with multiple " \
                        "fitness functions."
                    raise Exception(s)

        # Parse grammar file and set grammar class.
        params['BNF_GRAMMAR'] = CustomGrammar(path.join("..", "grammars", params['GRAMMAR_FILE']))

        # Population loading for seeding runs (if specified)
        if params['TARGET_SEED_FOLDER']:

            # Import population loading function.
            from operators.initialisation import load_population

            # A target folder containing seed individuals has been given.
            params['SEED_INDIVIDUALS'] = load_population(
                params['TARGET_SEED_FOLDER'])

        elif params['REVERSE_MAPPING_TARGET']:
            # A single seed phenotype has been given. Parse and run.

            # Import GE LR Parser.
            from scripts import GE_LR_parser

            # Parse seed individual and store in params.
            params['SEED_INDIVIDUALS'] = [GE_LR_parser.main()]


def set_param_imports():
    """
    This function makes the command line experience easier for users. When
    specifying operators listed in the lists below, users do not need to
    specify the full file path to the functions themselves. Users can simply
    specify a single word, e.g.

        "--mutation subtree"

    Using the special_ops dictionary for example, this will default to
    "operators.mutation.subtree. Executes the correct imports for specified
    modules and then saves the correct parameters in the params dictionary.
    Users can still specify the full direct path to the operators if they so
    desire, allowing them to create new operators and save them wherever
    they like.

    Sets the fitness function for a problem automatically. Fitness functions
    must be stored in fitness. Fitness functions must be classes, where the
    class name matches the file name.

    :return: Nothing.
    """

    # For these ops we let the param equal the function itself.
    ops = {'operators': ['INITIALISATION', 'SELECTION', 'CROSSOVER',
                         'MUTATION', 'REPLACEMENT'],
           'utilities.fitness': ['ERROR_METRIC'],
           'fitness': ['FITNESS_FUNCTION'],
           'algorithm': ['SEARCH_LOOP', 'STEP']}

    # We have to take 'algorithm' first as the functions from
    # algorithm need to be imported before any others to prevent
    # circular imports. We have to take 'utilities.fitness' before
    # 'fitness' because ERROR_METRIC has to be set in order to call
    # the fitness function constructor.

    for special_ops in ['algorithm', 'utilities.fitness',
                        'operators', 'fitness']:

        if all([callable(params[op]) for op in ops[special_ops]]):
            # params are already functions
            pass

        else:

            for op in ops[special_ops]:

                if special_ops == "fitness":
                    # Fitness functions represent a special case.

                    get_fit_func_imports()

                elif params[op] is not None:
                    # Split import name based on "." to find nested modules.
                    split_name = params[op].split(".")

                    if len(split_name) > 1:
                        # Check to see if a full path has been specified.

                        # Get attribute name.
                        attr_name = split_name[-1]

                        try:
                            # Try and use the exact specified path to load
                            # the module.

                            # Get module name.
                            module_name = ".".join(split_name[:-1])

                            # Import module and attribute and save.
                            params[op] = return_attr_from_module(module_name,
                                                                 attr_name)

                        except Exception:
                            # Either a full path has not actually been
                            # specified, or the module doesn't exist. Try to
                            # append specified module to default location.

                            # Get module name.
                            module_name = ".".join([special_ops,
                                                    ".".join(split_name[:-1])])

                            try:
                                # Import module and attribute and save.
                                params[op] = return_attr_from_module(module_name,
                                                                     attr_name)

                            except Exception:
                                s = "utilities.algorithm.initialise_run." \
                                    "set_param_imports\n" \
                                    "Error: Specified %s function not found:" \
                                    " %s\n" \
                                    "       Checked locations: %s\n" \
                                    "                          %s\n" \
                                    "       Please ensure parameter is " \
                                    "specified correctly." % \
                                    (op.lower(), attr_name, params[op],
                                     ".".join([module_name, attr_name]))
                                raise Exception(s)

                    else:
                        # Just module name specified. Use default location.

                        # If multi-agent is specified need to change
                        # how search and step module is called
                        # Loop and step functions for multi-agent is contained
                        # inside algorithm search_loop_distributed and
                        # step_distributed respectively

                        if( op == 'SEARCH_LOOP' and params[op] == 'search_loop_with_metrics'):
                            module_name = 'wrappers.search_loop_wrapper'
                            attr_name = 'search_loop'

                        elif( op == 'STEP' and params[op] == 'step_with_metrics'):
                            module_name = 'wrappers.step_wrapper'
                            attr_name = 'step'

                        elif params['MULTIAGENT'] and \
                        ( op == 'SEARCH_LOOP' or op == 'STEP' ) :
                            # Define the directory structure for the multi-agent search
                            # loop and step
                            multiagent_ops = {'search_loop':'distributed_algorithm.search_loop' \
                                                ,'step':'distributed_algorithm.step'}

                            # Get module and attribute names
                            module_name = ".".join([special_ops, multiagent_ops[op.lower()]])
                            attr_name = split_name[-1]

                        else:
                            # Get module and attribute names.
                            module_name = ".".join([special_ops, op.lower()])
                            attr_name = split_name[-1]

                        # Import module and attribute and save.
                        params[op] = return_attr_from_module(module_name,
                                                         attr_name)


def get_fit_func_imports():
    """
    Special handling needs to be done for fitness function imports,
    as fitness functions can be specified a number of different ways. Notably,
    a list of fitness functions can be specified, indicating multiple
    objective optimisation.

    Note that fitness functions must be classes where the class has the same
    name as its containing file. Fitness functions must be contained in the
    `fitness` module.

    :return: Nothing.
    """

    op = 'FITNESS_FUNCTION'

    if "," in params[op]:
        # List of fitness functions given in parameters file.

        # Convert specified fitness functions into a list of strings.
        params[op] = params[op].strip("[()]").split(",")

    if isinstance(params[op], list) and len(params[op]) == 1:
        # Single fitness function given in a list format. Don't use
        # multi-objective optimisation.
        params[op] = params[op][0]

    if isinstance(params[op], list):
        # List of multiple fitness functions given.

        for i, name in enumerate(params[op]):

            # Split import name based on "." to find nested modules.
            split_name = name.strip().split(".")

            # Get module and attribute names.
            module_path = ".".join(['fitness', name.strip()])
            attr = split_name[-1]

            # Import this fitness function.
            params[op][i] = return_attr_from_module(module_path, attr)

        # Import base multi-objective fitness function class.
        from fitness.base_ff_classes.moo_ff import moo_ff

        # Set main fitness function as base multi-objective fitness
        # function class.
        params[op] = moo_ff(params[op])

    else:
        # A single fitness function has been specified.

        # Split import name based on "." to find nested modules.
        split_name = params[op].strip().split(".")

        # Get attribute name.
        attr_name = split_name[-1]

        # Get module name.
        module_name = ".".join(["fitness_functions", params[op]])

        # Import module and attribute and save.

        try:
            # Import module.
            module = importlib.import_module(module_name)

        except ModuleNotFoundError:
            s = "utilities.algorithm.initialise_run.return_attr_from_module\n" \
                "Error: Specified module not found: %s" % (module_name)
            raise Exception(s)

        try:
            # Import specified attribute and return.
            params[op] = getattr(module, attr_name)

        except AttributeError:
            s = "utilities.algorithm.initialise_run.return_attr_from_module\n" \
                "Error: Specified attribute '%s' not found in module '%s'." \
                % (attr_name, module_name)
            raise Exception(s)

        # Initialise fitness function.
        params[op] = params[op]()
