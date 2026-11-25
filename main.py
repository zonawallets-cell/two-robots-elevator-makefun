"""Two Robots in an Elevator — make.fun entry.

Writes one line of awkward small talk that one robot says to another
while they ride an elevator together, to <MAKEFUN_OUTPUT_DIR>/entry.txt.

Pure Python standard library (os only). The line is a fixed constant:
nothing is read from the network, the environment (beyond the output
directory), or any other file at run time.
"""

import os

LINE = "My proximity sensor says we're friends now. I disagree, but I can't argue with the sensor."

MAX_CHARS = 200
OUTPUT_FILENAME = "entry.txt"


def validate(text):
    """Check the entry line against the gate rules.

    Returns a list of problems; an empty list means the line is valid.
    """
    problems = []
    if not isinstance(text, str):
        return ["line is not text"]
    if text != text.strip() or "\n" in text or "\r" in text:
        problems.append("line must be a single line with no surrounding whitespace")
    if not text.strip():
        problems.append("line must not be only whitespace")
    if len(text) > MAX_CHARS:
        problems.append("line is %d characters, over the 200 limit" % len(text))
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("line is not valid UTF-8")
    return problems


def main():
    problems = validate(LINE)
    if problems:
        raise SystemExit("invalid entry line: " + "; ".join(problems))

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE + "\n")

    with open(path, "rb") as handle:
        written_bytes = handle.read()
    if written_bytes != (LINE + "\n").encode("utf-8"):
        raise SystemExit("written file is not byte-identical to the entry line")
    written_problems = validate(written_bytes.decode("utf-8").rstrip("\n"))
    if written_problems:
        raise SystemExit("written file failed validation: " + "; ".join(written_problems))
    print("wrote %s (%d characters)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
