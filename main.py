#!/usr/bin/env python3
"""Hand-in program for the make.fun bounty "Sum up 23 November's
world news in one image" (Python 3.13, standard library only).

The entry itself is entry.png, the newspaper front page sitting next
to this file: one page that sums up Monday 23 November 2026. All this
program does is deliver those bytes, untouched, to the output folder,
so the grader receives exactly the image that build_image.py composed
and that the README shows.

Where the output folder is:
  - the grader's container: /output
  - anywhere else: set MAKEFUN_OUTPUT_DIR, e.g.
        mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRY_IMAGE = HERE / "entry.png"


def deliver() -> Path:
    """Copy the front page into the output folder and return its path.

    The copy is verified before it counts as delivered: the bytes in
    the output folder must be exactly as many as the bytes beside
    main.py, because the grader reads the image's format and size
    from the file itself and a truncated copy would fail silently.
    """
    if not ENTRY_IMAGE.is_file():
        raise SystemExit(f"no entry.png beside main.py (looked in {HERE})")
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / ENTRY_IMAGE.name
    shutil.copyfile(ENTRY_IMAGE, destination)
    expected = ENTRY_IMAGE.stat().st_size
    delivered = destination.stat().st_size
    if delivered != expected:
        raise SystemExit(
            f"copy went wrong: {destination} holds {delivered} bytes, "
            f"the entry image has {expected}"
        )
    return destination


if __name__ == "__main__":
    handed_in = deliver()
    print(f"delivered {handed_in} ({handed_in.stat().st_size} bytes)")
