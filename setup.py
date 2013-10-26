#!/usr/bin/env python

import sys
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as _readme:
    README = _readme.read()

with open(os.path.join(here, 'NEWS.txt')) as _news:
    NEWS = _news.read()

version = '0.2'

install_requires = [
    'GitPython>=0.3.2RC1']

if sys.version_info < (2, 7):
    install_requires.append('argparse>=1.2.1')

setup(name='git-sweep',
      version=version,
      description='Clean up branches from your Git remotes',
      long_description=README + '\n\n' + NEWS,
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
      author='Arc90, Inc.',
      author_email='',
      url='http://arc90.com',
      license='MIT',
      scripts=['git-sweep'])
