import argparse


def parser():
    """
    This function parses data from comand line.
    Returns the arguments.
    """
    parser = argparse.ArgumentParser(
        prog='task4',
        description='some description here')
    parser.add_argument('path1',
                        type=str,
                        help='path to students.json')

    parser.add_argument('path2',
                        type=str,
                        help='path to rooms.json')

    parser.add_argument('format',
                        type=str,
                        help='output format')

    args = parser.parse_args()

    return args
