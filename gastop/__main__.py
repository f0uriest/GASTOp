import numpy as np
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

    con = best.edges.copy()
    matl = best.properties.copy()

    # remove self connected edges and duplicate members
    matl = matl[(con[:, 0]) >= 0]
    con = con[(con[:, 0]) >= 0]
    matl = matl[(con[:, 1]) >= 0]
    con = con[(con[:, 1]) >= 0]
    con = con.astype(int)

    np.set_printoptions(precision=2)

    print('\n')
    print('Nodes:')
    print('     x     y     z   ')
    print(best.rand_nodes)

    print('\n')
    print('Edges:')
    print(con)

    print('\n')
    print('Properties:')
    print(matl)

    print('\n')
    print('Mass: %.3f kg' % best.mass)

    print('\n')
    print('FoS:')
    print(best.fos)

    print('\n')
    print('Deflections (m): ')
    print('      Dx        Dy        Dz        Rx        Ry        Rz        ')
    print(best.deflection[:, :, 0])

    if progress_display == 2:
        best.plot(domain=config['random_params']['domain'].T,
                  loads=config['evaluator_params']['boundary_conditions']['loads'],
                  fixtures=config['evaluator_params']['boundary_conditions']['fixtures'],
                  deflection=True, load_scale=.001, def_scale=100)


if __name__ == '__main__':
    main(sys.argv[1:])
