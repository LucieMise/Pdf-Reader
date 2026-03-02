# PDF Reader & Manipulation CLI

A lightweight Python CLI to read and manipulate PDF documents.

## Features

- Extract text from PDF pages
- Merge multiple PDFs into one file
- Split selected pages into a new PDF
- Rotate all pages or selected pages

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python pdf_tools.py --help
```

### Extract text

```bash
python pdf_tools.py extract-text input.pdf --output output.txt
```

If `--output` is omitted, text is printed to stdout.

### Merge PDFs

```bash
python pdf_tools.py merge merged.pdf part1.pdf part2.pdf part3.pdf
```

### Split pages

```bash
python pdf_tools.py split input.pdf section.pdf "1,3,5-7"
```

### Rotate pages

Rotate every page:

```bash
python pdf_tools.py rotate input.pdf rotated.pdf 90
```

Rotate only selected pages:

```bash
python pdf_tools.py rotate input.pdf rotated.pdf 180 --pages "1,2,10-12"
```
