[//]: # (Copyright © 2024 eContriver LLC)

# Initial Configuration

## Install `pyenv`

To manage Python versions use `pyenv`:
```shell
# MacOS
brew install pyenv
# Ubuntu
sudo apt-get install pyenv
```

To make it so `pyenv` sets the version when you enter the directory, add the following to the `.bashrc` or `.zshrc` file:
```shell
# .bashrc or .zshrc
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```
Start a new shell (run `zsh` or `bash` again) for these changes to take effect.

> Perhaps this works too (haven't tried it yet):
> ```shell
> eval "$(pyenv init --path)"
> ```

## Change to the project directory

Make sure to change into the project directory for most of the remaining commands:
```shell
cd capital-copilot
```

## Install `python`

To install the version of Python on the host system (any project could use this version):
```shell
pyenv install 3.12
```

### Switch to the new version of Python

To set the version of Python for this specific project:
```shell
# Only if .python-version doesn't exist, run:
pyenv local 3.12
```
_NOTE: This will create the `.python-version` file. Now changing into this directory will set the Python version._

For several IDEs (Codespace and PyCharm) the version of Python is set from this file automatically.

## Install `poetry`

Switch to the correct version of Python:
```shell
python --version
# If it is not right, then run:
pyenv shell 3.12
```

The shell has the correct version of Python. Now install `poetry` to the current version of Python:
```shell
pip install --upgrade pip
pip install poetry
```
_NOTE: If you switch to a different version of Python, then you will need to install `poetry` again for that version._


## Configure `poetry` 

Setup Poetry to create the virtual environment in the project directory, else it is created in the home directory:
```shell
# Check the current setting:
poetry config virtualenvs.in-project
# Set it to true if it is not already set:
poetry config virtualenvs.in-project true
```

## Setup `poetry` for this project (only if there isn't a pyproject.toml file)

Initialize the poetry project:
```shell
# If there isn't a pyproject.toml file, then run:
poetry init
```

Tell poetry what version of python is expected for this project:
```shell
# If the pyproject.toml file already has a python version, then skip this step:
poetry env use 3.12
```

----
# Using the Environment

## Start the poetry shell (our virtual environment)

Drop into the poetry shell for this project:
```shell
poetry shell
```

If you already have dependencies added, then you can install the dependencies:
```shell
poetry install --no-root
```

# For PyCharm

Select new interpreter and choose the one created by poetry. It will be in the `.venv` directory within this project.
If you don't see the `.venv` project, then make sure that you ran `poetry config virtualenvs.in-project true` (above).
```shell
.venv/bin/python
```
