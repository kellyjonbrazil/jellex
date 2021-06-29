#!/bin/bash
# build jellex PIP package
# to install locally, run:   pip3 install jellex-x.x.tar.gz

python3 setup.py sdist bdist_wheel
