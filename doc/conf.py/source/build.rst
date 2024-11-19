.. build

============
Build Module
============

1. Consider Using Environment
=============================

Python PEP 405 proposes Virtual Environments. Think about using.

2. Clone Repository
===================

.. code-block:: bash

    git clone https://github.com/clauspruefer/python-dbpool.git
    cd python-dbpool

3. Build As Non Root User
=========================

.. code-block:: bash

    python3 setup.py sdist

4. Install As Root User
=======================

.. code-block:: bash

    sudo pip3 install ./dist/package-0.1.tar.gz

or global on restrictive PIP package manager systems ...

.. code-block:: bash

    sudo pip3 install ./dist/package-0.1.tar.gz --break-system-packages

5. Run Tests
============

To ensure everything works correctly, run tests (after module installation).

.. code-block:: bash

    pytest
