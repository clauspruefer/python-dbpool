.. build

============
Build Module
============

Consider Using Environment
==========================

Python PEP 405 proposes Virtual Environments. Think about using.

Clone Repository
================

.. code-block:: bash

    git clone https://github.com/clauspruefer/python-dbpool.git
    cd python-dbpool

Build As Non Root User
======================

.. code-block:: bash

    python3 setup.py sdist

Install As Root User
====================

.. code-block:: bash

    sudo pip3 install ./dist/package-0.1.tar.gz

or global on restrictive PIP package manager systems ...

.. code-block:: bash

    sudo pip3 install ./dist/package-0.1.tar.gz --break-system-packages

Run Tests
=========

To ensure everything works correctly, run tests (after module installation).

.. code-block:: bash

    pytest
