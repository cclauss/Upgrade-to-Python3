# Upgrade to Python3
A GitHub Action that will upgrade your Python code to Python 3

This action uses [__flake8__](http://flake8.pycqa.org) to know if your Python code has syntax errors.

If syntax errors are found then this Action uses [__futurize__](http://python-future.org/futurize_cheatsheet.html) create pull requests that upgrade that code to Python 3.

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
            GITHUB_TOKEN: [FILTERED]
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


# Error

Failure on __git push --set-upstream origin new_idea_2019_02_11_10_03_38__
* __refusing to allow an integration to create .github/main.workflow__
```
$ git config --global user.email "cclauss@me.com"
$ git config --global user.name "cclauss"
$ git remote add upstream https://github.com/cclauss/Upgrade-to-Python3-test.git
$ git remote -v
origin	https://github.com/cclauss/Upgrade-to-Python3-test.git (fetch)
origin	https://github.com/cclauss/Upgrade-to-Python3-test.git (push)
upstream	https://github.com/cclauss/Upgrade-to-Python3-test.git (fetch)
upstream	https://github.com/cclauss/Upgrade-to-Python3-test.git (push)
$ git checkout -b new_idea_2019_02_11_10_03_38
Switched to a new branch 'new_idea_2019_02_11_10_03_38'
$ git add new_idea_2019_02_11_10_03_38.md
$ ['git', 'commit', '-am"Add new_idea_2019_02_11_10_03_38"']
[new_idea_2019_02_11_10_03_38 075b76a] "Add new_idea_2019_02_11_10_03_38"
 1 file changed, 1 insertion(+)
 create mode 100644 new_idea_2019_02_11_10_03_38.md
$ git push --set-upstream origin new_idea_2019_02_11_10_03_38
To https://github.com/cclauss/Upgrade-to-Python3-test.git
 ! [remote rejected] new_idea_2019_02_11_10_03_38 -> new_idea_2019_02_11_10_03_38 (refusing to allow an integration to create .github/main.workflow)
error: failed to push some refs to 'https://github.com/cclauss/Upgrade-to-Python3-test.git'
Traceback (most recent call last):
  File "/upgrade_to_python3.py", line 51, in <module>
    main()
  File "/upgrade_to_python3.py", line 47, in main
    cmd('git push --set-upstream origin ' + idea_name)
  File "/upgrade_to_python3.py", line 27, in cmd
    result.check_returncode()  # will raise subprocess.CalledProcessError()
  File "/usr/local/lib/python3.7/subprocess.py", line 428, in check_returncode
    self.stderr)
subprocess.CalledProcessError: Command '['git', 'push', '--set-upstream', 'origin', 'new_idea_2019_02_11_10_03_38']' returned non-zero exit status 1.

```
