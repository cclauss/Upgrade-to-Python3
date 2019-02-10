#!/usr/bin/env python3

import os
import sys
from contextlib import contextmanager
from getpass import getuser
from subprocess import run
from typing import Iterable, Tuple, Union

from generate_commit_msg import generate_commit_msg

print(f"os.environ: {os.environ}")

DIR_BASE = "/github/workspace/"
NEW_BRANCH_NAME = "modernize-Python-2-codes"
URL_BASE = "https://github.com"
USERNAME = getuser()  # Does local username == GitHub username?!?
if USERNAME == 'root':
    USERNAME = 'cclauss'
print(f"USERNAME = {USERNAME}")

# https://github.com/PythonCharmers/python-future/blob/master/src/libfuturize/fixes/__init__.py
# An even safer subset of fixes than `futurize --stage1`
SAFE_FIXES = set("lib2to3.fixes.fix_" + fix for fix
                 in """apply except exec exitfunc funcattrs has_key idioms intern isinstance
                       methodattrs ne numliterals paren reduce renames repr standarderror
                       sys_exc throw tuple_params types xreadlines""".split())


@contextmanager
def cd(new_dir: str) -> None:
    """https://stackoverflow.com/questions/431684/how-do-i-change-directory-cd-in-python/24176022#24176022"""
    prev_dir = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(prev_dir)


def cmd(in_cmd: Union[str, Iterable[str]], check: bool = True) -> str:  # run command and return its output
    """Run a command and return its output or raise CalledProcessError"""
    print(f"cmd({in_cmd})")
    if isinstance(in_cmd, str):
        in_cmd = in_cmd.strip().split()
    result = run(in_cmd, capture_output=True, text=True)
    if check and result.returncode:
        print("\n".join(result.stderr.splitlines()))
        result.check_returncode()  # will raise subprocess.CalledProcessError()
    return "\n".join(result.stdout.splitlines())


def fork_repo() -> None:
    "Could click the 'fork' button using Selenum, or similar..."
    pass


def clone_repo(repo_name: str) -> str:
    myfork_url = "/".join((URL_BASE, USERNAME, repo_name))
    print(cmd(f"git clone {myfork_url}"))


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


def flake8_tests() -> str:
    return cmd("flake8 . --show-source --statistics --select=E999", check=False)


def checkout_new_branch(branch_name: str = "") -> str:
    branch_name = branch_name or NEW_BRANCH_NAME
    return cmd(f"git checkout -b {branch_name}")


def git_remote_add_upstream(upstream_url: str) -> str:
    return cmd(f"git remote add upstream {upstream_url}")


def futurizer(repo_dir: str) -> int:
    with cd(repo_dir):
        flake8_results = flake8_tests()
        print(f"flake8_results:\n{flake8_results}")
        if flake8_results:
            # git_remote_add_upstream(upstream_url)
            # checkout_new_branch(NEW_BRANCH_NAME)
            file_paths = files_with_print_issues(flake8_results)
            print(fix_print(file_paths))  # only files that are broken!
            print(fix_safe_fixes())  # all files
            diff = cmd("git diff")
            if diff:
                print(f"diff:\n{diff}")
                print(cmd(["git", "commit", "-am", generate_commit_msg(diff)]))
                print(cmd(f"git push --set-upstream origin {NEW_BRANCH_NAME}"))
            else:
                "diff is empty!"
            # assert diff0 == diff, f"diff0:\n {diff0}\ndiff:\n {diff}"
            print("Success!")
            print(cmd(f"open {upstream_url}"))


if __name__ == "__main__":
    repo = DIR_BASE
    assert repo, "Man, you gotta give me something to work with here."
    print(f"pwd: {cmd('pwd')}")
    print(f"repo: {repo}")
    futurizer(repo)
