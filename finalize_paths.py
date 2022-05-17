# -*- coding: utf-8 -*-
"""Finalize SVG file. It would take the following actions:
1. Grouping the connected paths into the same 'Path' object.

Created: 2022-05-10 Mike_Chen@wistron.com
"""
import argparse
import pyembroidery
import svgpathtools
from svgpathtools import svg2paths2, wsvg

INPUT_SVG_PATH = './SVG/Asset 3cubic_beizer_practice_1.svg'
OUTPUT_SVG_PATH = './SVG/test.svg'


pattern = pyembroidery.EmbPattern()


def complex2tuple(complex):
    """Convert the representation of coodinate from complex number to tuple.
    Args
        complex (complex): Coodinate represents in complex number.
    Returns
        (tuple): Coodinate represents in tuple.
    """
    x = complex.real
    y = complex.imag
    return x, y


def is_same_pt(pt1, pt2):
    """Compare two coordinates which represent in complex number. """
    diff_real = abs(pt1.real - pt2.real)
    diff_imag = abs(pt1.imag - pt2.imag)

    if diff_real<1e-1 and diff_imag<1e-1:
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


def draw_curve(pattern, path, pitch=2.5):
    """
    Args
        pattern (pyembroidery.EmbPattern):
        path (svgpathtools.Path):
        pitch (float): stitch length (mm) (default: 2.5)
    """
    stitches = []
    dt = pitch/path.length()
    t = 0
    while t <= 1:
        stitches.append(path.point(t))
        t += dt

    if path.length()%pitch:
        stitches.append(path.end)

    # add stitches on pattern
    stitches = map(complex2tuple, stitches)
    for x, y in stitches:
        pattern.add_stitch_absolute(pyembroidery.STITCH, x, y)

    return stitches


def find_intersections(path1, path2):
    """Find intersections between path1 and path2. The order of these intersections follows parameterization of path1 (ascending).
    Args
        path1 (svgpathtools.Path): path object 1.
        path2 (svgpathtools.Path): path object 2.
    Returns
        (svgpathtools.Path): intersections between path1 and path2. Returns 'None' when there are no intersections.
    """
    intersections = []
    for (T1, seg1, t1), (T2, seg2, t2) in path1.intersect(path2):
        intersections.append([T1, path1.point(T1)])
        # print(T1, path1.point(T1), seg1.point(t1))

    if len(intersections)==0:
        return None

    # sort list according to T1 (parameterization of the path)
    intersections.sort(key=lambda x: x[0])
    return [i[1] for i in intersections]


def draw_line_halfway(pattern, path1, path2, pitch):
    """
    Args
    
    Returns
    
    """
    intersections = find_intersections(path1, path2)
    
    # comcatenate endpoints and intersections
    # pts = [path1.start] + intersections + [path1.end]
    # print(pts)


def main(args):

    paths, attributes, svg_attributes = svg2paths2(args.input_path)

    # paths = group_paths(paths, attributes)
    # wsvg(paths, svg_attributes=svg_attributes, filename=args.output_path)


    # intersections = find_intersections(paths[1], paths[2])

    # draw_line_halfway(None, paths[1], paths[2], pitch=1)
    
    draw_curve(pattern, paths[0])

    # write out
    pyembroidery.write_dst(pattern, args.input_path +'.dst')



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