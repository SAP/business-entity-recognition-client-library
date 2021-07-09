#!/usr/bin/env bash
rm -rf dist
python -m pip install --user pylint twine pydoc-markdown==2.1.3
python setup.py sdist
python -m twine upload dist/*