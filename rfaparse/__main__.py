from .parsing import parse_summary_screen
from argparse import ArgumentParser
import json


def create_argparser():
    parser = ArgumentParser(prog="rfaparse")
    parser.add_argument("file")
    return parser


def main():
    argv = create_argparser().parse_args()
    file = argv.file
    result = parse_summary_screen(file)
    print(json.dumps(result.asdict()))


if __name__ == "__main__":
    main()
