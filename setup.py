from setuptools import setup, find_packages
import os

with open('README.rst', encoding='utf8') as f:
  readme = f.read()

with open('atlas/version.py') as f:
  version = f.readline().strip()[15:-1]

setup(
  name='atlas-core',
  version=version,
  description='An open-source assistant built for people',
  long_description=readme,
  url='https://github.com/atlassistant/atlas',
  author='Julien LEICHER',
  license='GPL-3.0',
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    'atlas-sdk==2.0.0',
    'transitions==0.6.4',
    'fuzzywuzzy==0.16.0',
  ],
  extras_require={
    'snips': [
      'snips-nlu==0.14.0',
    ],
  },
  entry_points={
    'console_scripts': [
      'atlas = atlas.cli:main',
      'atlas-check = atlas.cli:check',
      'atlas-web = atlas.cli:web',
      'atlas-client = atlas.cli:client',
    ]
  },
)