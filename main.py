"""Worst Fix Ever: Funniest Commit Message.

Writes one commit-message line to /output/entry.txt: a bug fix that made
everything worse. Stdlib only, deterministic, no network, no file reads,
no model calls, no environment access.
"""
import sys
from pathlib import Path

ENTRY_TEXT = "fix: slow search by returning zero results instantly"
DEFAULT_OUTPUT = "/output/entry.txt"


def validate(text):
    """Gate (RULES.txt): UTF-8 str of 1-100 chars, not only whitespace, one line."""
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= 100:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def validate_bytes(data):
    """Gate on raw bytes: must decode as UTF-8, then pass validate()."""
    if not isinstance(data, (bytes, bytearray)):
        return False
    try:
        text = bytes(data).decode("utf-8")
    except UnicodeDecodeError:
        return False
    return validate(text)


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    out_path = Path(argv[1]) if len(argv) > 1 else Path(DEFAULT_OUTPUT)
    if not validate(ENTRY_TEXT):
        print("error: ENTRY_TEXT fails the 1-100 char gate", file=sys.stderr)
        return 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(ENTRY_TEXT.encode("utf-8"))
    # Read back and re-check the exact bytes on disk: a partial or
    # re-encoded write must never silently ship an invalid entry.
    if not validate_bytes(out_path.read_bytes()):
        print("error: written output fails the gate", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
