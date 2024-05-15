#!/bin/bash

# pip install twine # if twine is not installed
# pip install setuptools wheel # if wheel is not installed
python setup.py sdist bdist_wheel
twine upload dist/* --verbose