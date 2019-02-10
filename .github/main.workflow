workflow "New workflow" {
  on = "push"
  resolves = ["Find Python 3 syntax errors and undefined names"]
}

action "Find Python 3 syntax errors and undefined names" {
  secrets = ["GITHUB_TOKEN"]
  uses = "cclauss/Find-Python-syntax-errors-action@master"
}
