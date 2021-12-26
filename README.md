# Geography Weighter

A tool to weight input data by geography.

This tool helps you solve the problem "I have this data by postcode, and I'd like to have it by federal electorate".

## Development Environment

- pyenv for python versioning
- setup here <https://github.com/pyenv/pyenv>
- pipenv for virtual environment
- setup taken from this guide <https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c>, as well as https://dev.to/py3course/setting-up-a-python-environment-in-2020-3e9e
- I am developing in WSL on a windows machine, and am making use of this vscode extension to remotely run python <https://code.visualstudio.com/docs/remote/wsl-tutorial>

### Get started

- clone the repo
- ensure you have pipenv installed
- run `pipenv install --dev`
- run `pipenv shell` to get a shell in a virtual environment
- run the app with `pipenv run python app.py --help`

### Run tests

- `pipenv run pytest -v tests.py`

### Check test coverage
- `pipenv run pytest --cov=guts --cov=. tests/ --cov-config=.coveragerc --cov-report=xml`
- `pipenv run coverage report -m`


### Commit changes
- in the root of the git repo
- `pre-commit install`
- then use git as normal

## Ackowledgements

Setup from: <https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c>, https://dev.to/py3course/setting-up-a-python-environment-in-2020-3e9e

Gitignore: <https://github.com/github/gitignore/blob/master/Python.gitignore>

Tests influenced by: <https://semaphoreci.com/community/tutorials/testing-python-aapplications-with-pytest>,
<https://tryexceptpass.org/article/pytest-github-integration/>

CLI influenced by: <https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df>

Code structure influenced by: <https://levelup.gitconnected.com/raise-the-bar-of-code-quality-in-python-projects-7c49743f004f>
