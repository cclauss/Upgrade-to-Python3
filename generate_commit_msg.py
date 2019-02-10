#!/usr/bin/env python3

from collections import namedtuple
from typing import Iterable

msg = namedtuple("msg", "head body")

lookup = {"except": msg("Old style exceptions --> new style for Python 3",
                        "Old style exceptions are syntax errors in Python 3 "
                        "but new style exceptions work as expected in both Python "
                        "2 and Python 3."),
          "exec": msg("Use __exec()__ function in both Python 2 and Python 3",
                      "__exec()__ is a function in Python 3."),
          "print": msg("Use __print()__ function in both Python 2 and Python 3",
                       "Legacy __print__ statements are syntax errors in Python 3 "
                       "but __print()__ function works as expected in both Python "
                       "2 and Python 3.")}


def find_fixer(minus_text, plus_text):
    for func in ("exec", "print"):
        if (f"{func} " in minus_text and
                f"{func}(" not in minus_text and
                f"{func}(" in plus_text):
            return func
    if ("except " in minus_text and
            " as " not in minus_text and
            " as " in plus_text):
        return "except"


def generate_body(fixers: Iterable[str]) -> str:
    messages = (lookup[fixer] for fixer in fixers)
    return "\n".join(f"* {msg.head}\n    * {msg.body}" for msg in messages)


def generate_commit_msg(diff_text):
    fixers = []
    texts = {"-": "", "+": ""}
    for line in diff_text.splitlines():
        current = line[0] if line else " "
        if current in "-+":
            texts[current] += line[1:] + " "
        elif texts["-"] or texts["+"]:
            print("\n".join(f"{key}: {value}"for key, value in texts.items()))
            fixer = find_fixer(texts["-"], texts["+"])
            texts["-"] = texts["+"] = ""
            print(fixer)
            if fixer and fixer not in fixers:  # fixers is like an ordered set
                fixers.append(fixer)
                if fixers == lookup.keys():  # we got them all!
                    break

    if len(fixers) == 1:
        message = lookup[fixers[0]]
        title = message.head.replace("__", "")
        body = message.body
    else:
        title = "Modernize Python 2 code to get ready for Python 3"
        body = generate_body(fixers)
    return "\n\n".join((title, body))


if __name__ == "__main__":
    with open("tensorflow_models.diff") as in_file:
        print(generate_commit_msg(in_file.read()))
