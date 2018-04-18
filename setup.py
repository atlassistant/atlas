from setuptools import setup

setup(
  name='atlas',
  version='0.1.0',
  packages=['atlas'],
  install_requires=[
    'atlas_sdk==0.1.0',
    'transitions==0.6.4',
    'Flask==0.12.2',
    'Flask-RESTful==0.3.6',
    'Flask-SocketIO==2.9.6',
    'PyYAML==3.12',
  ],
)