"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from codecs import open

from setuptools import setup, find_packages


def get_version():
    with open('version.txt') as ver_file:
        version_str = ver_file.readline().rstrip()
    return version_str


setup(name='business-entity-recognition',
      version=get_version(),
      packages=find_packages(
          exclude=['examples*']),
      description='Exposes easy consumable methods via a client library, to access and use the API offerings of the AI '
                  'BUS Service - Business Entity Recognition.',
      author_email='komal.narsinghani@sap.com',
      maintainer='DL ML Apps BLR Prasanna DR',
      maintainer_email='DL_5CEDF333B4A5864B89BE0EE5@global.corp.sap'
      )
