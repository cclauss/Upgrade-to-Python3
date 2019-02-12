#!/usr/bin/env python3

import json
import os
import sys
from subprocess import run
from typing import Iterable, Tuple, Union

from generate_commit_msg import generate_commit_msg

print('=' * 83)  # Mark the start of Python execution in the Action logfile

NEW_BRANCH_NAME = "modernize-Python-2-codes"

# https://github.com/PythonCharmers/python-future/blob/master/src/libfuturize/fixes/__init__.py
# An even safer subset of fixes than `futurize --stage1`
SAFE_FIXES = set("lib2to3.fixes.fix_" + fix for fix
                 in """apply except exec exitfunc funcattrs has_key idioms intern isinstance
                       methodattrs ne numliterals paren reduce renames repr standarderror
                       sys_exc throw tuple_params types xreadlines""".split())


def cmd(in_cmd: Union[str, Iterable[str]], check: bool = True) -> str:  # run command and return its output
    """Run a command and return its output or raise CalledProcessError"""
    print('$', in_cmd)
    if isinstance(in_cmd, str):
        in_cmd = in_cmd.split()
    result = run(in_cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())
    if check:
        result.check_returncode()  # will raise subprocess.CalledProcessError()
    return '\n'.join(result.stdout.splitlines())


def flake8_tests() -> str:
    return cmd("flake8 . --show-source --statistics --select=E999", check=False)


def files_with_print_issues(flake8_results: str) -> Tuple[str]:
    """Walk backwards through flake8 output to find those files that have old style print statements."""
    file_paths = set()
    next_line_contains_file = False
    # reverse the lines so we can move from last to first
    for line in reversed(flake8_results.splitlines()):
        if next_line_contains_file:
            file_paths.add(line.split(":")[0])
        next_line_contains_file = "print " in line
    return tuple(sorted(file_paths))


def fix_print(file_paths: Iterable[str]) -> str:
    if not file_paths:
        return ""
    return cmd("futurize -f libfuturize.fixes.fix_print_with_import -w " +
               " ".join(file_paths))


def fix_safe_fixes() -> str:
    """This is an even safer subset of futurize --stage1 -w ."""
    return cmd(f"futurize -f {' -f '.join(SAFE_FIXES)} "
               "-f libfuturize.fixes.fix_next_call -w .")


# def checkout_new_branch(branch_name: str = "") -> str:
#     branch_name = branch_name or NEW_BRANCH_NAME
#     return cmd(f"git checkout -b {branch_name}")


# def git_remote_add_upstream(upstream_url: str) -> str:
#     return cmd(f"git remote add upstream {upstream_url}")


assert NEW_BRANCH_NAME not in cmd('git branch'), (
    f'The branch {NEW_BRANCH_NAME} is already present and must be deleted.')
assert os.getenv('GITHUB_TOKEN'), (
    '.github/main.workflow must provide access to the secret GITHUB_TOKEN.')

# print('os.environ: ' + '\n            '.join(f'{key}: {os.getenv(key)}'
#                                              for key in sorted(os.environ)))

with open(os.getenv("GITHUB_EVENT_PATH")) as in_file:
    github_event = json.load(in_file)
# print(json.dumps(github_event, sort_keys=True, indent=2))

flake8_results = flake8_tests()
assert flake8_results, "No Python 3 syntax errors or undefined names were found."

cmd("git checkout -b " + NEW_BRANCH_NAME)
cmd('git config --global user.email "{head_commit[author][email]}"'.format(**github_event))
cmd('git config --global user.name "{head_commit[author][name]}"'.format(**github_event))
file_paths = files_with_print_issues(flake8_results)
diff = fix_print(file_paths) if file_paths else fix_safe_fixes()
push_result = ""
if '+' in diff:
    cmd('git rm .github/main.workflow')  # GitHub Actions bug: See issue #1
    cmd(["git", "commit", "-am", generate_commit_msg(diff)])
    push_result = cmd("git push --set-upstream origin " + NEW_BRANCH_NAME)
else:
    print("diff is empty!")
print("Success!")
print('\n'.join(line for line in push_result.replace('remote:') if line))
print(push_result.replace('remote:'))
