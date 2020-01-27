# Upgrade to Python3
A GitHub Action that will upgrade your Python code to Python 3

This action uses [__flake8__](http://flake8.pycqa.org) to know if your Python code has syntax errors.

If syntax errors are found then this Action uses [__futurize__](http://python-future.org/futurize_cheatsheet.html) create pull requests that gradually upgrade that code to be more compatible with Python 3.  After this Action has run, return to your repo and look for a "__modernize-Python-2-codes__" branch in your repo.  If this branch exists then select it and __make pull request__ and make sure that your automate tests pass before merging the pull request.  After merging, delete the "__modernize-Python-2-codes__" branch so that the process can be repeated.

Example workflow (Put the following text into your repo's `.github/workflows/upgrade-to-py3.yml`):
```
on:
  push:
    branches:
      - master

jobs:
  upgrade_to_Python3::
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: "Upgrade to Python3"
        uses: cclauss/Upgrade-to-Python3@master
      - name: Commit files
        run: |
              git config --local user.email "me@me.me"
              git config --local user.name "GitHub Action"
              git commit -m "Add changes" -a
      - name: Push changes
        uses: peter-evans/create-pull-request@v2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: 'py3-addendum'
```

* https://github.com/marketplace/actions/upgrade-to-python-3
* https://blog.jessfraz.com/post/the-life-of-a-github-action
* https://developer.github.com/actions/creating-github-actions
