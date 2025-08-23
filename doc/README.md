# Documentation (Sphinx)

This document provides instructions for building the Sphinx documentation for the Python DB Pool module.

## 1. Dependencies

### 1.1. Sphinx Basic HTML / RTD Theme

Install the required Sphinx packages for HTML documentation generation:

```bash
# install sphinx and read the docs theme
apt-get install python3-sphinx python3-sphinx-rtd-theme
```

### 1.2. PDF / LaTeX

Install LaTeX packages for PDF documentation generation:

```bash
# install complete latex distribution for pdf generation
apt-get install texlive-full
```

## 2. Build

### 2.1. HTML Documentation

Build HTML documentation and navigate to the output directory:

```bash
# generate html documentation
make html

# navigate to the generated html files
cd ./build/html/
```

### 2.2. PDF / LaTeX

Build PDF documentation and navigate to the output directory:

```bash
# generate pdf documentation using latex
make latexpdf

# navigate to the generated pdf files
cd ./build/latex/
```
