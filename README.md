# Upgrade-to-Python3
A GitHub Action that will upgrade your Python code to Python 3

This action uses [__flake8__](http://flake8.pycqa.org) to know if your Python code has syntax errors.

If syntax errors are found then this Action uses [__futurize__](http://python-future.org/futurize_cheatsheet.html) create pull requests that upgrade that code to Python 3.

Those pull requests are created and submitted using [__pygithub3__](https://pygithub3.readthedocs.io).

Example workflow (Put the following text into `.github/main.workflow`):
```
workflow "New workflow" {
  on = "push"
  resolves = ["Upgrade to Python 3"]
}

action "Upgrade to Python 3" {
  uses = "cclauss/Upgrade-to-Python3@master"
}
```
* https://blog.jessfraz.com/post/the-life-of-a-github-action
* https://developer.github.com/actions/creating-github-actions/accessing-the-runtime-environment/
```
os.environ: GITHUB_ACTION: Upgrade to Python 3
            GITHUB_ACTOR: cclauss
            GITHUB_EVENT_NAME: push
            GITHUB_EVENT_PATH: /github/workflow/event.json
            GITHUB_REF: refs/heads/master
            GITHUB_REPOSITORY: cclauss/Upgrade-to-Python3-test
            GITHUB_SHA: <<< stuff >>>
            GITHUB_WORKFLOW: New workflow
            GITHUB_WORKSPACE: /github/workspace
            GPG_KEY: <<< stuff >>>
            HOME: /github/home
            HOSTNAME: 2c6c2018c55f
            LANG: C.UTF-8
            PATH: /usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
            PYTHON_PIP_VERSION: 19.0.1
            PYTHON_VERSION: 3.7.2
```
