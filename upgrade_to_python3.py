#!/usr/bin/env python3

import json
import os

from datetime import datetime as dt
from subprocess import run
from typing import Iterable, Tuple, Union

assert os.getenv('GITHUB_TOKEN'), 'Need access to the secret GITHUB_TOKEN.'
with open(os.getenv("GITHUB_EVENT_PATH")) as in_file:
    github_event = json.load(in_file)
# print(json.dumps(github_event, sort_keys=True, indent=2))


def cmd(in_cmd: Union[str, Iterable[str]], check: bool = True) -> str:  # run command and return its output
    """Run a command and return its output or raise CalledProcessError"""
    print('cmd({}):'.format(in_cmd))
    if isinstance(in_cmd, str):
        in_cmd = in_cmd.strip().split()
    result = run(in_cmd, capture_output=True, text=True)
    if result.stdout:
        print('\n'.join('  out> ' + line for line in result.stdout.splitlines()))
    if result.stderr:
        print('\n'.join('  err> ' + line for line in result.stderr.splitlines()))
    if check:
        result.check_returncode()  # will raise subprocess.CalledProcessError()
    return '\n'.join(result.stdout.splitlines())


def main() -> None:
    cmd('git config --global user.email "{head_commit[author][email]}"'.format(**github_event))
    cmd('git config --global user.name "{head_commit[author][name]}"'.format(**github_event))
    cmd('git remote add upstream https://github.com/' + os.getenv('GITHUB_REPOSITORY'))
    cmd('git remote -v')

    idea_name = 'new_idea_{:%Y_%m_%d_%H_%M_%S}'.format(dt.now())
    file_name = idea_name + '.md'  # new_idea_2019_02_11_06_39_02.md

    cmd('git checkout -b ' + idea_name)
 
    with open(file_name, 'w') as out_file:
        out_file.write('# My new idea is ' + idea_name)

    cmd('git add ' + file_name)
    cmd(['git', 'commit', f'-am"Add {idea_name}"'])
    cmd('git push --set-upstream origin ' + idea_name)


if __name__ == "__main__":
    main()
