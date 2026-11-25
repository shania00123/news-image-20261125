#!/usr/bin/env python3
"""Copy the shipped poster to the grader output path.

Standard library only. The output directory is MAKEFUN_OUTPUT_DIR when set,
otherwise the first command-line argument when given, otherwise /output.
"""

import os
import struct
import sys
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
EXPECTED_SIZE = (1024, 1024)


def output_dir() -> Path:
    env_value = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_value:
        return Path(env_value)
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return Path("/output")


def checked_png_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError("poster.png exceeds the 1 MiB limit")
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("poster.png is not a PNG")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("poster.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        raise ValueError(f"poster.png is {width}x{height}, expected 1024x1024")
    return data


def main() -> int:
    source = Path(__file__).resolve().with_name("poster.png")
    data = checked_png_bytes(source)
    destination_dir = output_dir()
    destination_dir.mkdir(parents=True, exist_ok=True)
    (destination_dir / "entry.png").write_bytes(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
