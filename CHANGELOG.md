# Changelog

## Version 1.0.1

### Bug Fixes

- **Default Configuration Values**: Added default values for optional database configuration parameters
  - `query_timeout`: Default 5000 milliseconds (5 seconds)
  - `session_tmp_buffer`: Default 128 MB
  - `ssl`: Default 'disable'
  - `connect_timeout`: Default 10 seconds
  - Fixes issue where example `01-logical-replication` would not work without explicit configuration

### Changes

- **Connection Retry**: Removed configurable connect retry sleep time
  - Connection retry sleep time is now statically set to 1 second
  - Simplifies configuration by removing `connection_retry_sleep` parameter

### Documentation

- **Configuration Documentation**: Updated configuration documentation to reflect correct units and types
  - Corrected `query_timeout` unit from Seconds to Milliseconds
  - Corrected `ssl` type from boolean to enum (disable|allow|prefer|require)
  - Updated default values to match implementation
  - Simplified multi-database configuration examples to show only required parameters

### CI/CD

- **GitHub Actions**: Added GitHub Actions CI workflow
  - Runs tests on push and pull request events
  - Includes pytest with coverage reporting
  - Validates module build and installation

## Version 1.0 (Stable)

- Stable release tested and verified
- All features from Version 1.0rc1 are now production-ready

## Version 1.0rc1

### Major Features

- **Multi-Database Support**: Added support for multiple database endpoints with automatic load balancing
  - Configure multiple database hosts in configuration
  - Connections automatically distributed across available endpoints

- **Threading Models**: Support for both threaded and non-threaded deployment scenarios
  - `threaded` mode (default): Thread-safe connection handling with locks for traditional multi-threaded web servers
  - `non-threaded` mode: Removes locking overhead for single-threaded applications, eliminating GIL contention
  - Configurable threading model via configuration

- **FalconAS Compatibility**: Full compatibility with FalconAS Python Application Server
  - 1 Process == 1 Python Interpreter (threading-less) model
  - Effectively solves GIL issues through non-threaded configuration mode
  - Optimized for process-per-request architectures

### Architecture & Performance

- **Configuration Enhancements**: 
  - Threading model configuration

### Documentation & Development

- **Documentation**: Complete rewrite of documentation to reflect new features
  - Comprehensive Sphinx-based documentation
  - Configuration guides and examples

- **API Improvements**: Better error handling and connection management
  - Enhanced exception handling with specific error classes
  - Improved connection iteration and management
  - Improved threading-model stability / thread locking

- **Testing**: Added pytest-based unit test suite
  - Tests for threaded and non-threaded connection handling
  - Tests for single and multiple database endpoint configurations
  - Tests for connection rotation and pool management

- **CI/CD**: Added GitHub Actions workflow
  - Pylint code analysis for Python 3.8, 3.9, and 3.10

## Version 0.99

- Add Handler.commit() procedure used for autocommit=False connections

## Version 0.98rc1

- Finish Documentation including Docstrings
- Fix Metadata

