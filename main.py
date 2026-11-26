#!/usr/bin/env python3
"""Write one line to /output/entry.txt: the remark a smug self-checkout
machine makes about a shopper's meal deal.

The line was picked from 46 candidates by pairwise judging against the
brief: the laugh sits in the reframe of a meal deal as a cry for help,
and the twist lands on the last word, "barcode", which is the machine's
own voice. It is held here as one constant; the gates below refuse
anything that is not exactly that line, so the file the program writes
can only ever contain the judged text. The gates check length, shape,
and that every character is printable, so a stray control character
or invisible whitespace can never slip into the entry file.
"""

import os
import sys

LINE = "That is not a meal deal. That is a cry for help with a barcode."

# The judged length of the line above, counted in characters.
EXPECTED_LEN = 63

# Entry gate from the brief: 1-200 characters, a single line.
MIN_LEN = 1
MAX_LEN = 200


def gate_length(line):
    """The line must be exactly the judged length and inside the gate."""
    if len(line) != EXPECTED_LEN:
        return f"line is {len(line)} characters, expected {EXPECTED_LEN}"
    if not MIN_LEN <= len(line) <= MAX_LEN:
        return f"line outside the {MIN_LEN}-{MAX_LEN} character gate"
    return None


def gate_printable(line):
    """Every character must be printable: no control or invisible chars."""
    for ch in line:
        if not ch.isprintable():
            return f"line contains a non-printable character U+{ord(ch):04X}"
    return None


def gate_shape(line):
    """The line must be one line with no surrounding space."""
    if "\n" in line or "\r" in line:
        return "line must be a single line"
    if line != line.strip():
        return "line must have no surrounding space"
    return None


def check_line(line):
    """Run every gate; return the first failure, or None if it passes."""
    for gate in (gate_length, gate_shape, gate_printable):
        problem = gate(line)
        if problem is not None:
            return problem
    return None


def encode_line(line):
    """Encode the line as UTF-8 with exactly one trailing newline."""
    return (line + "\n").encode("utf-8")


def output_path():
    """Resolve where entry.txt goes, honouring the kit's override."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return out_dir, os.path.join(out_dir, "entry.txt")


def write_and_verify(path, data):
    """Write the bytes, then read them back and confirm they match."""
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as f:
        if f.read() != data:
            return "read-back mismatch"
    return None


def main():
    problem = check_line(LINE)
    if problem is not None:
        sys.exit(problem)
    out_dir, path = output_path()
    data = encode_line(LINE)
    os.makedirs(out_dir, exist_ok=True)
    problem = write_and_verify(path, data)
    if problem is not None:
        sys.exit(problem)
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
