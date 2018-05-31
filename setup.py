from setuptools import setup
import os

with open('README.md', encoding='utf8') as f:
  readme = f.read()

with open('atlas/version.py') as f:
  version = f.readline().strip()[15:-1]

setup(
  name='atlas-core',
  version=version,
  description='An open-source assistant built for people',
  long_description_content_type='text/markdown',
  long_description=readme,
  url='https://github.com/atlassistant/atlas',
  author='Julien LEICHER',
  license='GPL-3.0',
  packages=['atlas', 'atlas.client', 'atlas.interpreters', 'atlas.web'],
  include_package_data=True,
  install_requires=[
    'atlas-sdk==1.1.8',
    'transitions==0.6.4',
    'Flask==0.12.2',
    'Flask-RESTful==0.3.6',
    'Flask-SocketIO==2.9.6',
    'PyYAML==3.12',
    'fuzzywuzzy==0.16.0',
  ],
  extras_require={
    'snips': [
      'snips-nlu==0.13.5',
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