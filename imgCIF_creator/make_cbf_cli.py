import sys
import os
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from dxtbx.model.experiment_list import ExperimentListFactory

from .core import make_cbf

def create_new_template(old_template):
    """
    Derive a new directory for CBF files
    """
    old_path, old_fn = os.path.split(old_template)
    one_dir_missing = os.path.split(old_path)[0]
    new_dir = os.path.join(one_dir_missing, "CBF")
    i = 0
    while os.path.isdir(new_dir):
        i += 1
        new_dir = os.path.join(one_dir_missing, f"CBF{i}")

    os.mkdir(new_dir)
    no_ext = os.path.splitext(old_fn)
    new_fn = no_ext[0] + ".cbf"
    return os.path.join(new_dir, new_fn)

def parse_commandline(argv):

    ap = ArgumentParser(prog="make_cbf")
    ap.add_argument(
        "input_dir",
        type=Path,
        nargs='+',
        help="Directory containing files to convert"
    )
    ap.add_argument(
        '--overload-value',
        help="Overload value to include in CBF file"
    )
    ap.add_argument(
        '--frame-limit',
        type=int,
        default=None,
        help="Convert no more than this many frames."
        )
    args = ap.parse_args(argv)

    return args

def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    args = parse_commandline(argv)

    expts = ExperimentListFactory.from_filenames(args.input_dir)
    fullpath = expts.imagesets()[0].get_template()

    # Create our own template in sibling "CBF" directory

    out_fn = create_new_template(fullpath)
    
    make_cbf(expts, out_fn, overload_value=args.overload_value, frame_limit=args.frame_limit)


if __name__ == '__main__':
    main()
