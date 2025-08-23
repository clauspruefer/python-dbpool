# Python PostgreSQL Database Connection Pool (pgdbpool)

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

pgdbpool is a Python library providing PostgreSQL database connection pooling functionality with support for multiple endpoints, load balancing, and flexible threading models. The library is designed for Web/Application Server environments.

## Working Effectively

**Bootstrap development environment (REQUIRES NETWORK ACCESS):**
- `python3 -m venv pgdbpool-dev` -- creates virtual environment in ~3 seconds
- `source pgdbpool-dev/bin/activate` -- activates virtual environment  
- `pip install --upgrade pip` -- upgrades pip (may fail due to network timeouts)
- `pip install psycopg2-binary` -- installs PostgreSQL adapter (~6 seconds, REQUIRED)
- `pip install pytest pytest-cov` -- installs testing framework (~9 seconds, REQUIRED for testing)
- `pip install pylint` -- installs code quality checker (~8 seconds, REQUIRED for CI compliance)
- `pip install build` -- installs build tools (~6 seconds, may fail due to network timeouts)
- `pip install sphinx sphinx-rtd-theme` -- installs documentation tools (~16 seconds, may fail due to network timeouts)

**CRITICAL**: All pip installations may fail with "Read timed out" errors in network-restricted environments. These are not code issues but infrastructure limitations.

**Development installation:**
- `ln -s $(pwd)/src $(pwd)/pgdbpool` -- creates symlink for package import (use absolute paths)
- Use `PYTHONPATH=.` when running commands to ensure proper module importing
- **CANNOT run library without psycopg2 dependency** - import will fail with "No module named 'psycopg2'"

**Run tests (REQUIRES psycopg2-binary, pytest dependencies):**
- `PYTHONPATH=. pytest test/unit/test_pool.py -v` -- runs all unit tests (~3.3 seconds, 6 tests)
- `PYTHONPATH=. pytest --cov=pgdbpool --cov-report=html test/unit/test_pool.py` -- runs tests with coverage (~3.4 seconds)
- Tests use mocked PostgreSQL connections and do NOT require actual database setup
- All tests should PASS - if they don't, the issue is likely with your environment setup
- **WILL FAIL** if dependencies are not installed: "No module named 'pgdbpool'" or "No module named 'pytest'"

**Code quality (REQUIRES pylint dependency):**
- `pylint --max-line-length=120 --disable=C0103,C0114,C0115,C0116,C0209,R0801,R0903,R0205,R1737,R0913,W0611,W0707,W1202,W0246,W0223,W0221,W0104,W0102,W0613,E0401,E0611,E1101 $(git ls-files 'src/pool.py')` -- runs pylint as per CI workflow (~1.3 seconds)
- Code should achieve 10.00/10 pylint score
- ALWAYS run this command before submitting changes as it matches the CI pipeline
- **WILL FAIL** if pylint is not installed: "command not found: pylint"

**Build package (NETWORK DEPENDENT - may fail in restricted environments):**
- `python -m build --sdist` -- creates source distribution (may fail due to network timeouts)
- `python -m build --wheel` -- creates wheel distribution (may fail due to network timeouts)
- **WARNING**: Build process requires network access to download dependencies and may timeout
- If build fails with "Read timed out" errors, this is due to network connectivity limitations

**Documentation (REQUIRES sphinx dependencies):**
- `cd doc/conf.py && sphinx-build -b html source build/html` -- builds HTML documentation (~0.8 seconds)
- Documentation builds successfully but with warnings about missing pgdbpool module (expected)
- Built docs are located in `doc/conf.py/build/html/index.html`
- **WILL FAIL** if sphinx is not installed: "command not found: sphinx-build"

## Validation

**ALWAYS run these validation steps after making code changes:**
1. **Run unit tests**: `PYTHONPATH=. pytest test/unit/test_pool.py -v` (should pass all 6 tests)
2. **Check code quality**: Run the exact pylint command above (should score 10.00/10)
3. **Test functionality**: Create a simple test script to validate library imports and basic functionality
4. **Build documentation**: Verify docs still build successfully

**Manual functionality test template:**
```python
import sys
sys.path.insert(0, '/path/to/repo/src')
import pool

# Test basic import and configuration
config = {
    'db': {
        'host': '127.0.0.1', 'name': 'testdb', 'user': 'testuser', 'pass': 'testpass',
        'ssl': 'require', 'connect_timeout': 30, 'connection_retry_sleep': 1,
        'query_timeout': 30, 'session_tmp_buffer': 128
    },
    'groups': {
        'test_group': {'connection_count': 2, 'autocommit': False}
    }
}

# Mock the database connection for testing
# [Add mock objects as needed]

pool.Connection.init(config)
# Test database operations with pool.Handler('test_group')
```

## Important Timing and Constraints

**NEVER CANCEL these operations:**
- Dependency installations: Can take 5-16 seconds each depending on package size
- Tests: Complete in ~3.3 seconds, always wait for completion
- Pylint analysis: Completes in ~1.3 seconds
- Documentation build: Completes in ~0.8 seconds

**Network dependencies that may fail:**
- Package building with `python -m build` (requires internet access)
- Installing packages with pip (if PyPI is unreachable)
- Always use pre-installed `psycopg2-binary` instead of building from source

**File structure notes:**
- Source code is in `src/pool.py` and `src/__init__.py`
- Tests are in `test/unit/test_pool.py`
- Package configuration is in `pyproject.toml`
- CI configuration is in `.github/workflows/pylint.yaml`

## Common Tasks

**Repository structure:**
```
/home/runner/work/python-dbpool/python-dbpool/
├── src/
│   ├── __init__.py
│   └── pool.py                    # Main library code
├── test/
│   └── unit/
│       └── test_pool.py          # Unit tests (6 tests)
├── doc/
│   └── conf.py/
│       └── source/               # Sphinx documentation source
├── pyproject.toml                # Modern Python packaging
├── setup.py                      # Legacy packaging
├── .github/
│   └── workflows/
│       └── pylint.yaml          # CI pipeline (Python 3.8, 3.9, 3.10)
└── README.md                     # Project documentation
```

**Key package features to understand:**
- **Connection pooling**: Manages PostgreSQL connections with configurable pool sizes
- **Multi-endpoint support**: Load balances across multiple database servers
- **Threading models**: Supports both threaded and non-threaded configurations
- **Transaction control**: Manual commit support for complex operations
- **Configuration-driven**: Uses Python dictionaries for flexible setup

**Development workflow:**
1. Set up virtual environment and install dependencies
2. Create symlink for package imports
3. Make code changes in `src/pool.py`
4. Run tests with proper PYTHONPATH
5. Check code quality with pylint
6. Validate functionality with manual testing
7. Build documentation if needed

**Environment variables for testing (not needed for unit tests):**
- `TEST_DB_HOST`, `TEST_DB_NAME`, `TEST_DB_USER`, `PSQL_PWD` (only for integration testing with real databases)