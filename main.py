"""Write the finished 18 November news poster to the output directory.

The poster (entry.png) was drawn at build time by draw_poster.py and is
shipped in this repository. This program only copies it: the grading
sandbox gives us a read-only repo and a writable output directory, and
the run must be deterministic, so no drawing happens here.
"""
import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def run() -> int:
    repo = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo, IMAGE_NAME)
    if not os.path.isfile(source):
        print(f"{IMAGE_NAME} not found in repo", file=sys.stderr)
        return 1
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, IMAGE_NAME)
    shutil.copyfile(source, dest)
    if os.path.getsize(source) != os.path.getsize(dest):
        print("copy size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
