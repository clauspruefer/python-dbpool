# Python PostgreSQL Database Connection Pool (pgdbpool)

pgdbpool is a Python library providing PostgreSQL database connection pooling functionality with support for multiple endpoints, load balancing, and flexible threading models.

## Quick Setup

**Basic development environment:**
```bash
python3 -m venv pgdbpool-dev
source pgdbpool-dev/bin/activate
pip install psycopg2-binary pytest pylint
```

**Run tests:**
```bash
PYTHONPATH=. pytest test/unit/test_pool.py -v
```

**Check code quality:**
```bash
pylint --max-line-length=120 --disable=C0103,C0114,C0115,C0116,C0209,R0801,R0903,R0205,R1737,R0913,W0611,W0707,W1202,W0246,W0223,W0221,W0104,W0102,W0613,E0401,E0611,E1101 src/pool.py
```

## File Structure

- `src/pool.py` - Main library code  
- `test/unit/test_pool.py` - Unit tests
- `pyproject.toml` - Package configuration

## Key Features

- Connection pooling for PostgreSQL databases
- Multi-endpoint support with load balancing  
- Configurable threading models
- Transaction control with manual commit support