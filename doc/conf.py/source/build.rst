.. build

=================
Building pgdbpool
=================

Guide for building pgdbpool from source code.

1. Development Environment Setup
================================

**Virtual Environment (Recommended)**

Python PEP 405 virtual environments provide isolated development environments:

.. code-block:: bash

    # Create virtual environment
    python3 -m venv pgdbpool-dev
    source pgdbpool-dev/bin/activate  # Linux/macOS
    # pgdbpool-dev\Scripts\activate   # Windows

    # Upgrade pip
    pip install --upgrade pip

2. Source Code Acquisition
===========================

**Clone from GitHub:**

.. code-block:: bash

    git clone https://github.com/clauspruefer/python-dbpool.git
    cd python-dbpool

**Download Release Archive:**

.. code-block:: bash

    # Download latest release
    wget https://github.com/clauspruefer/python-dbpool/archive/refs/tags/v1.0rc1.tar.gz
    tar -xzf v1.0rc1.tar.gz
    cd python-dbpool-1.0rc1

3. Install Dependencies
=======================

**Runtime Dependencies:**

.. code-block:: bash

    # Install PostgreSQL adapter
    pip install psycopg2-binary
    
    # Or compile from source (requires libpq-dev)
    # apt-get install libpq-dev  # Debian/Ubuntu
    # pip install psycopg2

**Development Dependencies:**

.. code-block:: bash

    # Install testing framework
    pip install pytest pytest-cov
    
    # Install documentation tools (optional)
    pip install sphinx sphinx-rtd-theme

4. Build Distribution Package
=============================

**Create Source Distribution:**

.. code-block:: bash

    # Modern way using build
    pip install build
    python -m build --sdist

    # Legacy way using setuptools
    python setup.py sdist

**Create Wheel Distribution:**

.. code-block:: bash

    python -m build --wheel

5. Installation Methods
=======================

**Development Installation (Editable):**

.. code-block:: bash

    # Install in development mode
    pip install -e .

**Local Package Installation:**

.. code-block:: bash

    # Install from built package
    pip install dist/pgdbpool-1.0rc1.tar.gz

**System-wide Installation:**

.. code-block:: bash

    # Install system-wide (requires sudo)
    sudo pip install dist/pgdbpool-1.0rc1.tar.gz
    
    # For restrictive systems
    sudo pip install dist/pgdbpool-1.0rc1.tar.gz --break-system-packages

6. Testing
==========

**Run Test Suite:**

.. code-block:: bash

    # Run all tests
    pytest
    
    # Run with coverage report
    pytest --cov=pgdbpool --cov-report=html
    
    # Run specific test file
    pytest test/unit/test_pool.py

**Test Configuration:**

Tests require a PostgreSQL database. Set environment variables:

.. code-block:: bash

    export PSQL_PWD="your_test_db_password"
    export TEST_DB_HOST="localhost"
    export TEST_DB_NAME="test_database"
    export TEST_DB_USER="test_user"

7. Documentation Building
=========================

**Build HTML Documentation:**

.. code-block:: bash

    cd doc/conf.py
    sphinx-build -b html source build/html

**View Documentation:**

.. code-block:: bash

    # Open in browser
    open build/html/index.html  # macOS
    xdg-open build/html/index.html  # Linux
