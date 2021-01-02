from os import path
from socket import gethostname

hostname = gethostname().split('.')
machine_name = hostname[0]

from algorithm.parameters import params, load_params
from wrapper.custom_grammar import CustomGrammar


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
    from utilities.algorithm.initialise_run import set_param_imports
    from utilities.fitness.math_functions import return_one_percent
    from utilities.algorithm.command_line_parser import parse_cmd_args
    from utilities.stats import trackers, clean_stats

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
        params['BNF_GRAMMAR'] = CustomGrammar(path.join("..", "grammars",
                                                         params['GRAMMAR_FILE']))

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