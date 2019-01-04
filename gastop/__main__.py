"""Runs the gastop program
This file runs scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.

"""
import argparse
import sys
from gastop import GenAlg, utilities


def parse_args(args):
    """Parses command line arguments

    Args:
        args (list): List of arguments to parse, ie sys.argv

    Returns:
        parsed_args (argparse object): argparse object containing parsed arguments.
    """

    parser = argparse.ArgumentParser(prog='gastop',
                                     description="A Genetic Algorithm for Structural Design and Topological Optimization. See full documentation at gastop.readthedocs.io")
    parser.add_argument("config_path", help="file path to gastop config file")
    parser.add_argument("-p", "--pop_size", type=int,
                        help="population size. If not specified, defaults to what is in config.", metavar='')
    parser.add_argument("-g", "--num_gens", type=int,
                        help="number of generations. If not specified, defaults to what is in config.", metavar='')
    parser.add_argument("-t", "--num_threads", type=int,
                        help="number of threads to use. If not specified, defaults to what is in config.", metavar='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--quiet", action="store_true",
                       help="hide progress display window")
    group.add_argument("-d", "--display", action='store_true',
                       help="show progress display window")
    return parser.parse_args(args)


def main(args=sys.argv[1:]):
    """Runs the main GASTOp script, from the command line.

    Reads and parses user input from command line, runs the code,
    and prints and plots the resulting best truss.
    """

    args = parse_args(args)
    config = utilities.init_file_parser(args.config_path)

    if args.display:
        progress_display = 2
    elif args.quiet:
        progress_display = 1
    else:
        progress_display = None

    if args.num_threads:
        num_threads = args.num_threads
    else:
        num_threads = config['ga_params']['num_threads']

    if args.num_gens:
        num_generations = args.num_gens
    else:
        num_generations = config['ga_params']['num_generations']

    if args.pop_size:
        pop_size = args.pop_size
    else:
        pop_size = config['ga_params']['pop_size']

    # Create the Genetic Algorithm Object
    ga = GenAlg(config)
    ga.initialize_population(pop_size)
    best, progress_history = ga.run(num_generations=num_generations,
                                    progress_display=progress_display,
                                    num_threads=num_threads)

    print(best)

    if progress_display == 2:
        best.plot(domain=config['random_params']['domain'].T,
                  loads=config['evaluator_params']['boundary_conditions']['loads'],
                  fixtures=config['evaluator_params']['boundary_conditions']['fixtures'],
                  deflection=True)


if __name__ == '__main__':
    main(sys.argv[1:])
