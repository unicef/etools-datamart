#!/usr/bin/env python
import ast
import codecs
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'etools_datamart', '__init__.py')

rel = lambda *args: os.path.join(ROOT, 'src', 'requirements', *args)  # noqa

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(content).group(1)))
    name = str(ast.literal_eval(_name_re.search(content).group(1)))


def fread(fname):
    return open(rel(fname)).read()


readme = codecs.open('README.md').read()

setup(name=name,
      version=version,
      description="""UNICEF eTools Datamart""",
      long_description=readme,
      author='',
      author_email='',
      url='https://github.com/unicef/etools-datamart',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      license="Not open source",
      zip_safe=False,
      keywords='',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Django',
          'License :: OSI Approved :: MIT',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.6',
      ])
