# Upgrade to Python3
A GitHub Action that will upgrade your Python code to Python 3

This action uses [__flake8__](http://flake8.pycqa.org) to know if your Python code has syntax errors.

If syntax errors are found then this Action uses [__futurize__](http://python-future.org/futurize_cheatsheet.html) create pull requests that gradually upgrade that code to be more compatible with Python 3.  After this Action has run, return to your repo and look for a "__modernize-Python-2-codes__" branch in your repo.  If this branch exists then select it and __make pull request__ and make sure that your automate tests pass before merging the pull request.  After merging, delete the "__modernize-Python-2-codes__" branch so that the process can be repeated.

Example workflow (Put the following text into your repo's `.github/main.workflow`):
```
workflow "New workflow" {
  on = "push"
  resolves = ["Upgrade to Python 3"]
}

action "Upgrade to Python 3" {
  secrets = ["GITHUB_TOKEN"]
  uses = "cclauss/Upgrade-to-Python3@master"
}
```

* https://github.com/marketplace/actions/upgrade-to-python-3
* https://blog.jessfraz.com/post/the-life-of-a-github-action
* https://developer.github.com/actions/creating-github-actions
