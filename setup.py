#!/usr/bin/env python

"""Set up git-sweep."""

import ast
import os
from setuptools import setup


ROOT = os.path.abspath(os.path.dirname(__file__))


def version():
    """Return version string."""
    with open('git-sweep') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with open(os.path.join(ROOT, 'README.rst')) as _readme:
    README = _readme.read()

setup(name='git-sweep3k',
      version=version(),
      description='Clean up branches from your Git remotes',
      long_description=README,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Version Control',
          'Topic :: Text Processing'
      ],
      keywords='git maintenance branches',
      license='MIT',
      scripts=['git-sweep'])
