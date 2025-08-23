# Documentation (Sphinx)

This document provides instructions for building the Sphinx documentation for the Python DB Pool module.

## 1. Dependencies

### 1.1. Sphinx Basic HTML / RTD Theme

Install the required Sphinx packages for HTML documentation generation:

```bash
# Install Sphinx and Read the Docs theme
apt-get install python3-sphinx python3-sphinx-rtd-theme
```

### 1.2. PDF / LaTeX

Install LaTeX packages for PDF documentation generation:

```bash
# Install complete LaTeX distribution for PDF generation
apt-get install texlive-full
```

## 2. Build

### 2.1. HTML Documentation

Build HTML documentation and navigate to the output directory:

```bash
# Generate HTML documentation
make html

# Navigate to the generated HTML files
cd ./build/html/
```

### 2.2. PDF / LaTeX

Build PDF documentation and navigate to the output directory:

```bash
# Generate PDF documentation using LaTeX
make latexpdf

# Navigate to the generated PDF files
cd ./build/latex/
```
