#!/usr/bin/env python3
"""news-image-20261125 — entrypoint.

Copies the front page this repository ships (poster.png, drawn by
render.py) to the output directory as entry.png. Standard library only,
no network, no randomness: two runs write identical bytes.

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
It is never a relative folder: the grader reads /output/entry.png.
"""

import binascii
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
POSTER = os.path.join(HERE, "poster.png")
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def load_poster():
    """Read poster.png and check it is a whole 1024x1024 PNG."""
    with open(POSTER, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise ValueError("poster.png is %d bytes, over the 1 MiB limit"
                         % len(data))
    if data[:8] != PNG_MAGIC:
        raise ValueError("poster.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise ValueError("poster.png is %dx%d, expected 1024x1024"
                         % (width, height))
    # Walk every PNG chunk and verify its CRC, so a truncated or
    # corrupted poster is caught here instead of at the gate.
    pos = 8
    seen_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            raise ValueError("poster.png ends inside chunk %r" % ctype)
        stored = struct.unpack(">I", data[end - 4:end])[0]
        actual = binascii.crc32(ctype + data[pos + 8:end - 4]) & 0xFFFFFFFF
        if stored != actual:
            raise ValueError("poster.png chunk %r fails its CRC" % ctype)
        if ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                raise ValueError("poster.png has trailing bytes after IEND")
            break
        pos = end
    if not seen_iend:
        raise ValueError("poster.png has no IEND chunk")
    return data


def main():
    try:
        data = load_poster()
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)
    with open(target, "rb") as fh:
        if fh.read() != data:
            print("read-back mismatch on %s" % target, file=sys.stderr)
            return 1
    print("wrote %s (%d bytes)" % (target, len(data)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
