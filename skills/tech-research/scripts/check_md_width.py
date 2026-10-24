#!/usr/bin/env python3
"""Fail if a Markdown line is longer than the limit and could have been wrapped.

Run it after `mdformat --wrap N`: whatever is still too long then is either unbreakable
(table rows, code, URLs) and allowed, or a heading or text that a person must shorten.

Usage: check_md_width.py [--max N] FILE...
"""

import argparse
import re
import sys

URL = re.compile(r"<?https?://\S+?>?(?=[\s)\]]|$)")
FENCE = re.compile(r"^\s*(```|~~~)")
REF_DEF = re.compile(r"^\s*\[[^\]]+\]:\s")


def violations(path, limit):
    in_code = False
    with open(path, encoding="utf-8") as f:
        for no, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if FENCE.match(line):
                in_code = not in_code
                continue
            if in_code or len(line) <= limit:
                continue
            if line.lstrip().startswith("|") or REF_DEF.match(line):
                continue
            # A URL cannot be wrapped. The line is fine if it fits once each URL counts as one char.
            if len(URL.sub("u", line)) <= limit:
                continue
            yield no, len(line), line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=100)
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()
    failed = False
    for path in args.files:
        for no, length, line in violations(path, args.max):
            failed = True
            print(f"{path}:{no}: {length} > {args.max} chars: {line[:60]}...")
    if failed:
        print(f"Shorten or split these lines (headings cannot wrap). Limit: {args.max}.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
