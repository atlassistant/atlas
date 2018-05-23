from setuptools import setup

setup(
  name='atlas-core',
  version='1.0.0',
  description='An open-source assistant built for people',
  author='Julien LEICHER',
  license='GPL-3.0',
  packages=['atlas', 'atlas.client', 'atlas.interpreters', 'atlas.web'],
  include_package_data=True,
  install_requires=[
    'atlas-sdk==1.0.0',
    'transitions==0.6.4',
    'Flask==0.12.2',
    'Flask-RESTful==0.3.6',
    'Flask-SocketIO==2.9.6',
    'PyYAML==3.12',
    'fuzzywuzzy==0.16.0',
  ],
  entry_points={
    'console_scripts': [
      'atlas = atlas.cli:main',
      'atlas-check = atlas.cli:check',
      'atlas-web = atlas.cli:web',
      'atlas-client = atlas.cli:client',
    ]
  },
)