# pyaquael
A python library for the Aquael Leddy link unofficial API

## Usage
See [simple.py](examples/simple.py) for examples on using library through import.

This library can also be used from the command line:

```
Usage:
  aquael-cli poweron IPADDRESS RBW
  aquael-cli poweroff IPADDRESS
  aquael-cli (-h | --help)
  aquael-cli --version
```

## Build and push to PyPI

```
rm -rf dist
python3 -m build
python3 -m twine upload dist/*
```