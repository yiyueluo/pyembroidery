# -*- coding: utf-8 -*-
"""Finalize SVG file. It would take the following actions:
1. Grouping the connected paths into the same 'Path' object.

Created: 2022-05-10 Mike_Chen@wistron.com
"""
import argparse
import pyembroidery
import svgpathtools
from svgpathtools import svg2paths, wsvg

INPUT_SVG_PATH = './SVG/4x4_margin_practice_3.svg'
OUTPUT_SVG_PATH = './SVG/test2.svg'


def is_same_pt(pt1, pt2):
    """Compare two coordinates which represent in complex number. """
    diff_real = abs(pt1.real - pt2.real)
    diff_imag = abs(pt1.imag - pt2.imag)

    if diff_real<1e-5 and diff_imag<1e-5:
        return True
    return False


def group_paths(paths, attributes):
    """Grouping the connected paths into the same 'Path' object. If starting point coordinate of a line and ending point coordinate of another line are very close, stack the lines in the same 'Path' object.
    Args
        paths (list[svgpathtools.Path]): Existing paths of input SVG file.
        attributes (list[dict[str]]): Attributes of paths.
    """
    # TODO: Keep SVG attribute

    groups = [[]]
    group_id = 0
    segments = [seg for seg in paths[0]]
    groups[group_id].extend(segments)
    prev_path = paths[0]

    for i, path in enumerate(paths[1:]):
        # print(path.start, path.end)
        if not is_same_pt(path.start, prev_path.end):
            groups.append([])
            group_id += 1

        segments = [seg for seg in path]
        groups[group_id].extend(segments)
        prev_path = path

    # Wrap line segments by svgpathtools.Path
    new_paths = []
    for g in groups:
        new_paths.append(svgpathtools.Path(*g))

    return new_paths#, new_attributes


def main(args):

    paths, attributes = svg2paths(args.input_path)
    
    paths = group_paths(paths, attributes)

    # write out
    wsvg(paths, filename=args.output_path)


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='Visualize stitches.')
    parser.add_argument('--input_path', type=str, default=INPUT_SVG_PATH, help='Input file path')
    parser.add_argument('--output_path', type=str, default=OUTPUT_SVG_PATH, help='Output file path')
    parser.add_argument('--dryrun', action='store_true')
    return parser.parse_args()


if __name__=='__main__':
    args = parse_args()
    main(args)