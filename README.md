# pyaquael
A python library for the Aquael Leddy link unofficial API

## Usage
See [simple.py](examples/simple.py) for examples on using library through import.

This library can also be used from the command line. See `aquael-cli --help` for usage instructions

## Build and push to PyPI

```
rm -rf dist
python3 -m build
python3 -m twine upload dist/*
```

## Install local build

```
python3 -m pip install --force dist/pyaquael-0.5.0-py3-none-any.whl
```