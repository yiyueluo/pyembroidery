# -*- coding: utf-8 -*-
"""Convert DST file to SVG file.

Created: 2022-05-10 Mike_Chen@wistron.com
"""
import argparse
import pyembroidery


INPUT_PATH = './output/Asset 2palm.dst'
OUTPUT_PATH = './SVG/test.svg'


def main(args):
    pattern = pyembroidery.read_dst(args.input_path)
    pyembroidery.write_svg(pattern, args.output_path)
    print('{} -> {}'.format(args.input_path, args.output_path))


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='Convert file format.')
    parser.add_argument('--input_path', type=str, default=INPUT_PATH, help='Input file path')
    parser.add_argument('--output_path', type=str, default=OUTPUT_PATH, help='Output file path')
    parser.add_argument('--dryrun', action='store_true')
    return parser.parse_args()


if __name__=='__main__':
    args = parse_args()
    main(args)