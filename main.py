#!/usr/bin/env python3
"""Entry program for make.fun's "Sum up 19 November's world news in
one image" bounty (Python 3.13, standard library only).

The image is the entry.png beside this file: a one-page newspaper
front page drawn and typeset by build_image.py from the artwork in
assets/. This program's whole job is to copy those exact bytes to the
output, so every run writes the identical file.

In the grader's container the output is /output/entry.png; outside it,
MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def main():
    if not SOURCE.is_file():
        raise SystemExit(f"entry image missing beside main.py: {SOURCE}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
