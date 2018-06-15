atlas
=====

An open-source 🤖 assistant built for people. **atlas** is a totally **open-source**, **self-hosted**, **interoperable** assistant written in Python 3. It uses the MQTT protocol to communicate with third party components.

Ever wanted to build your own Alexa, Siri or Google Assistant and host it yourself? That's why **atlas** has been created!

Installation
------------

pip
~~~

.. code-block:: bash

  $ pip install atlas-core

source
~~~~~~

.. code-block:: bash

  $ git clone https://github.com/atlassistant/atlas.git
  $ cd atlas
  $ python setup.py install

Testing
-------

.. code-block:: bash

  $ cd tests/
  $ python -m unittest -v
