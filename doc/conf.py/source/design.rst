.. design

======
Design
======

1. Current Model
================

Common Web-Application-Server use a threaded or event-based (also threaded) model.
The following diagrams illustrate how the DB-Connection-Pool works in detail.

.. code-block:: bash

    +-----------------------------------------------------------------------------+
    | Web-Server  / ESB Middleware                                                |
    |-----------------------------------------------------------------------------+
    | Python-App / DB-Pool Module                                                 |
    |                                                                             |
    +-----------------------------------------------------------------------------+
    |  Script1.py (T1)  | Script1.py (T2)  | ScriptX.py (T3)  | ScriptX.py (T4)   |
    |  PCon1            | PCon2            | PCon3            | PCon4             |
    +-----------------------------------------------------------------------------+
             |                   |                  |                  |
    +-------------------+------------------+------------------+-------------------+
    |  Node 1 / Con 1   |  Node 1 / Con 2  |  Node 1 / Con 3  |  Node 1 / Con 4   |
    |-------------------+------------------+------------------+-------------------|
    | Database Cluster                                                            |
    +-----------------------------------------------------------------------------+

- Currently you must implement load sharing to multiple hosts by yourself.
- Also Python Global Interpreter Lock reduces Performance / Scaling.

2. Process Based / FalconAS
===========================

FalconAS is a high speed Python Application Server / Data-Aggregator Middleware.

.. code-block:: bash

    +-----------------------------------------------------------------------------+
    | Web-Server  / FalconAS / ESB Middleware                                     |
    |-----------------------------------------------------------------------------+
    | Python-App / DB-Pool Module                                                 |
    |                                                                             |
    +-----------------------------------------------------------------------------+
    |  Script1.py (P1)  | Script1.py (P2)  | Script2.py (P3)  | Script2.py (P4)   |
    |  1 Interpreter    | 1 Interpreter    | 1 Interpreter    | 1 Interpreter     |
    |  PCon1            | PCon2            | PCon3            | PCon4             |
    +-----------------------------------------------------------------------------+
             |                   |                  |                  |
    +-------------------+------------------+------------------+-------------------+
    |  Node 1 / Con 1   |  Node 1 / Con 2  |  Node 2 / Con 3  |  Node 2 / Con 4   |
    |-------------------+------------------+------------------+-------------------|
    | Database Cluster                                                            |
    +-----------------------------------------------------------------------------+

- 1 Client Request will be handled by a *static preloaded* Python Interpreter in 1 OS Process.
- 1 Process does not need DB Pooling because Client Requests are serial.
- 1 Process holds 1 DB Connection to 1 Backend Node (non-loadbalanced).
- Security is increased because of Process Segmentation / Separation. 
- Loadbalancing can easily be implemented into this model.

.. warning::

    This model currently is not supported by **pgdbpool** module but will be implemented in
    the next major release.

.. note::

    Loadbalancing will be implemented *transparently* for both models in a next major release.
