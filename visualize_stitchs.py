# -*- coding: utf-8 -*-
"""Visualize stitch points and curves.

Created: 2022-05-10 Mike_Chen@wistron.com
"""
import argparse
import pyembroidery
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import svgpathtools
from svgpathtools import svg2paths


INPUT_SVG_PATH = './SVG/4x4_margin_practice_3.svg'
# INPUT_SVG_PATH = './SVG/Asset 2palm.svg'
# INPUT_SVG_PATH = './SVG/test.svg'


def complex2tuple(complex):
    """Convert the representation of coodinate from complex number to tuple. The resulting coordinate would be moved from quardrant I to quardrant IV
    Args
        complex (complex): Coodinate represents in complex number.
    Returns
        (tuple): Coodinate represents in tuple.
    """
    x = complex.real
    y = -complex.imag
    return x, y


def visualize_drawing(file, show_ctrlpts=False):
    """Visualize stitches
    Matplotlib Bézier examples:
    https://matplotlib.org/3.5.0/tutorials/advanced/path_tutorial.html
    https://matplotlib.org/3.5.0/gallery/shapes_and_collections/path_patch.html
    Args
        file (str): SVG file path.
        show_ctrlpts (bool): Whether to display control points of Beizer curve or not (default: False).
    """
    paths, _ = svg2paths(file)
    fig, ax = plt.subplots()

    verts = []
    codes = []
    stitch_pts = []
    control_pts = []

    for path in paths:
        print(path)
        for seg in path:
            # every types of curve have endpoints (stitch points)
            start_endpts = complex2tuple(seg.start)
            end_endpts = complex2tuple(seg.end)
            stitch_pts.extend([start_endpts, end_endpts])

            if isinstance(seg, svgpathtools.Line):
                verts.extend([start_endpts, end_endpts])
                codes.extend([mpath.Path.MOVETO, mpath.Path.LINETO])

            elif isinstance(seg, svgpathtools.CubicBezier):
                # CubicBezier has 2 control points
                ctrl_pts1 = complex2tuple(seg.control1)
                ctrl_pts2 = complex2tuple(seg.control2)
                control_pts.extend([ctrl_pts1, ctrl_pts2])

                verts.extend([start_endpts, ctrl_pts1, ctrl_pts2, end_endpts])
                codes.extend([mpath.Path.MOVETO, mpath.Path.CURVE4,
                    mpath.Path.CURVE4, mpath.Path.CURVE4])
            else:
                # TODO: Implement Arc and QuadraticBezier handler later.
                print('Unseen type of curve object in the path. It could be Arc or QuadraticBezier.')

    patch = mpatches.PathPatch(mpath.Path(verts, codes),
        fc="none", transform=ax.transData)
    ax.add_patch(patch)

    xs, ys = zip(*stitch_pts)
    ax.plot(xs, ys, 'x', lw=2, color='red', ms=10)

    if show_ctrlpts:
        xs, ys = zip(*control_pts)
        ax.plot(xs, ys, 'x', lw=2, color='orange', ms=10)

    ax.set_title('Title')
    # ax.set_xlim(-0.1, 1.1)
    # ax.set_ylim(-0.1, 1.1)
    plt.show()


def main(args):

    visualize_drawing(args.input_path, True)


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='Visualize stitches.')
    parser.add_argument('--input_path', type=str, default=INPUT_SVG_PATH, help='Input SVG file path')
    # parser.add_argument('--dryrun', action='store_true')
    return parser.parse_args()


if __name__=='__main__':
    args = parse_args()
    main(args)