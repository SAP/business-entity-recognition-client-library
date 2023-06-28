"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(name='sap-business-entity-recognition-client-library',
      version=1.4,
      license='apache-2.0',
      install_requires=[
          'requests~=2.31'
      ],
      packages=find_packages(
          exclude=['examples*']),
      description='Exposes easy consumable methods via a client library, to access and use the API offerings of the AI '
                  'BUS Service - Business Entity Recognition.',
      author='Gokul Mohanarangan',
      author_email='gokumohan@gmail.com',
      url='https://github.com/SAP/business-entity-recognition-client-library',
      download_url='https://github.com/SAP/business-entity-recognition-client-library/archive/refs/heads/main.zip',
      maintainer='Gokul Mohanarangan',
      maintainer_email='gokumohan@gmail.com',
      keywords=['business', 'entity', 'recognition', 'machine learning', 'SAP', 'client', 'library'],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3'
          ],
      )
