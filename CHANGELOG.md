# Changelog

## Version 1.0rc1

### Major Features

- **Multi-Database Support**: Added support for multiple database endpoints with automatic load balancing
  - Configure multiple database hosts in configuration
  - Connections automatically distributed across available endpoints
  - Built-in load balancing for read operations
  - Read/write/endpoint group separation
  - Enhanced fault tolerance and scalability

- **Threading Models**: Support for both threaded and non-threaded deployment scenarios
  - `threaded` mode (default): Thread-safe connection handling with locks for traditional multi-threaded web servers
  - `non-threaded` mode: Removes locking overhead for single-threaded applications, eliminating GIL contention
  - Configurable threading model via configuration

- **FalconAS Compatibility**: Full compatibility with FalconAS Python Application Server
  - 1 Process == 1 Python Interpreter (threading-less) model
  - Effectively solves GIL issues through non-threaded configuration mode
  - Optimized for process-per-request architectures

### Architecture & Performance

- **Improved Architecture**: Enhanced connection handling and pool management
  - Automatic failover and reconnection capabilities
  - Connection health monitoring with SQL ping verification
  - Efficient connection reuse and reduced overhead
  - Flexible deployment configuration options

- **Configuration Enhancements**: 
  - Group-based connection configuration
  - Database connection property management
  - Threading model configuration
  - Session buffer and timeout controls

### Documentation & Development

- **Documentation**: Complete rewrite of documentation to reflect new features
  - Comprehensive Sphinx-based documentation
  - Configuration guides and examples

- **API Improvements**: Better error handling and connection management
  - Enhanced exception handling with specific error classes
  - Improved connection iteration and management

## Version 0.99

- Add Handler.commit() procedure used for autocommit=False connections

## Version 0.98rc1

- Finish Documentation including Docstrings
- Fix Metadata

