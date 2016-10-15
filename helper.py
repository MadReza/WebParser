import argparse

def get_cmd_args():
    """Helper function for analyzing arguments"""
    parser = argparse.ArgumentParser(description='Reuters Search')

    parser.add_argument(
        '-s',
        action="store",
        dest="'search_term'",
        help='The search term you want to find in the documents. Add quotes if you require multiple words.'
    )

    parser.add_argument(
        '-b',
        action="store",
        dest="block_size",
        type=int,
        default=0,
        help='Block Size limitation on the memory. Number specified will serve as a limiter for all tokens read and processed.'
    )
    
    """ Placeholder for reference and futur arguments
    parser.add_argument(
        '-t',
        action="store_true",
        dest="test",
        default=False,
        help="Test all variations of Algorithsm and Heuristics"
    )

    parser.add_argument(
        '-p',
        action="store",
        dest="thePuzzle",
        metavar='N',
        type=int,
        nargs=9,
        default=[1,2,3,4,0,5,6,7,8],
        help="The 8-puzzle required to be solved. 0 being the empty spot. e.g.: 1 2 3 4 0 8 7 6 5"
    )
    """
    return parser.parse_args()
