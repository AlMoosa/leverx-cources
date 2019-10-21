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

    parser.add_argument('host',
                        type=str,
                        help='database host')

    parser.add_argument('user',
                        type=str,
                        help='user login')

    parser.add_argument('password',
                        type=str,
                        help='user password')

    parser.add_argument('db',
                        type=str,
                        help='database name')

    args = parser.parse_args()

    return args
