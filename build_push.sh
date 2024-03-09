 #!/usr/bin/env bash
 rm -rf build
 rm -rf dist
 rm -rf pyaquael.egg-info
python3 setup.py bdist_wheel
twine upload dist/*