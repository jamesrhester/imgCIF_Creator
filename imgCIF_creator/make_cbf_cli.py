import sys
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from dxtbx.model.experiment_list import ExperimentListFactory

from .core import make_cbf

def parse_commandline(argv):

    ap = ArgumentParser(prog="make_cbf")
    ap.add_argument(
        "input_fn",
        type=Path,
        nargs='+',
        help="Experiment description in JSON format as produced by DIALS "
             "(typically '<input_fn>.expt') "
    )
    ap.add_argument(
        '--overload-value',
        help="Pixels with this value or above in the image data will be considered invalid"
    )
    args = ap.parse_args(argv)

    return args

def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    args = parse_commandline(argv)
    out_fn = args.output_file
    if not out_fn.suffix:
        out_fn = out_fn.with_suffix('.cif')

    frame_limit = np.inf if (args.frames_limit is None) else args.frames_limit

    if args.input_fn[0].suffix == '.expt':
        assert len(args.input_fn) == 1, "Please pass only 1 .expt file"
        expts = ExperimentListFactory.from_json_file(
            args.input_fn[0], check_format=True
        )

    with out_fn.open('w') as outf:
        make_cbf(expts, outf, out_fn.stem, locations,
                 overload_value=args.overload_value, frame_limit=frame_limit)


if __name__ == '__main__':
    main()
