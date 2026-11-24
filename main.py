#!/usr/bin/env python3
"""Write a deadpan one-star review of gravity to /output/entry.txt.

For the make.fun bounty "One-Star Review of Something Essential": one
single-line review, at most 160 characters, of an everyday essential,
deadpan throughout, no exclamation marks, with the turn in the last
few words.

Deterministic: no network, no clock, no randomness. The entry is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, prints the entry to
stdout, and enforces the competition gate: 1 to 160 characters, not only
white space. The entry is written by write_entry(), which creates the
output directory first; a failure to write is reported as one clean
line on stderr with a non-zero exit instead of a traceback.
"""

import os
import sys
from pathlib import Path

ENTRY = "One star for gravity. It never takes a day off, never calls in sick, and still drops my toast butter side down."

MIN_CHARS = 1
MAX_CHARS = 160
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def require_nonblank(text: str) -> None:
    """Reject an entry that is only white space."""
    if not text.strip():
        raise ValueError("entry is only white space")


def require_length(text: str) -> int:
    """Reject an entry outside the 1 to 160 character gate.

    Returns the character count. A blank-only entry fails on the
    white-space rule, not the length rule, so the message always says
    what is actually wrong.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-160")
    return chars


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 160 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    require_nonblank(text)
    return require_length(text)


def write_entry(path: Path, text: str) -> None:
    """Create the output directory and write the entry text to path.

    Raises OSError to the caller, which reports it cleanly instead of
    letting a traceback escape.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fail(message: str) -> int:
    """Report one clean error line on stderr and return exit code 1."""
    print(message, file=sys.stderr)
    return 1


def main() -> int:
    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        return fail(str(exc))

    path = resolve_output_path()
    try:
        write_entry(path, ENTRY)
    except OSError as exc:
        return fail(f"could not write {path}: {exc}")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
