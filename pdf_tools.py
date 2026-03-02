#!/usr/bin/env python3
"""Simple CLI for reading and manipulating PDF documents.

Features:
- Extract text
- Merge PDFs
- Split selected pages into a new PDF
- Rotate pages
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable



def _load_pypdf():
    try:
        from pypdf import PdfReader, PdfWriter
    except ModuleNotFoundError as exc:
        raise SystemExit("Missing dependency: pypdf. Install with `pip install -r requirements.txt`.") from exc
    return PdfReader, PdfWriter


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def extract_text(input_pdf: Path, output_txt: Path | None = None) -> str:
    PdfReader, _ = _load_pypdf()
    reader = PdfReader(str(input_pdf))
    parts: list[str] = []
    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        parts.append(f"\n--- Page {idx} ---\n{text}")

    result = "\n".join(parts).strip()
    if output_txt is not None:
        _ensure_parent(output_txt)
        output_txt.write_text(result, encoding="utf-8")
    return result


def merge_pdfs(inputs: Iterable[Path], output_pdf: Path) -> None:
    PdfReader, PdfWriter = _load_pypdf()
    writer = PdfWriter()
    for path in inputs:
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)

    _ensure_parent(output_pdf)
    with output_pdf.open("wb") as handle:
        writer.write(handle)


def split_pdf(input_pdf: Path, output_pdf: Path, pages: Iterable[int]) -> None:
    PdfReader, PdfWriter = _load_pypdf()
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()
    for page_number in pages:
        zero_based = page_number - 1
        if zero_based < 0 or zero_based >= len(reader.pages):
            raise ValueError(f"Page {page_number} out of range for {input_pdf}")
        writer.add_page(reader.pages[zero_based])

    _ensure_parent(output_pdf)
    with output_pdf.open("wb") as handle:
        writer.write(handle)


def rotate_pdf(input_pdf: Path, output_pdf: Path, angle: int, pages: Iterable[int] | None = None) -> None:
    if angle % 90 != 0:
        raise ValueError("Angle must be a multiple of 90")

    PdfReader, PdfWriter = _load_pypdf()
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()

    if pages is None:
        page_set = set(range(1, len(reader.pages) + 1))
    else:
        page_set = set(pages)

    for idx, page in enumerate(reader.pages, start=1):
        if idx in page_set:
            page.rotate(angle)
        writer.add_page(page)

    _ensure_parent(output_pdf)
    with output_pdf.open("wb") as handle:
        writer.write(handle)


def _parse_pages(raw: str) -> list[int]:
    pages: list[int] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", maxsplit=1)
            start, end = int(start_s), int(end_s)
            if end < start:
                raise ValueError(f"Invalid page range: {token}")
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(token))
    if not pages:
        raise ValueError("No pages were provided")
    return pages


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read and manipulate PDF documents")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_extract = subparsers.add_parser("extract-text", help="Extract text from a PDF")
    p_extract.add_argument("input", type=Path, help="Input PDF path")
    p_extract.add_argument("-o", "--output", type=Path, help="Optional output .txt path")

    p_merge = subparsers.add_parser("merge", help="Merge multiple PDFs into one")
    p_merge.add_argument("output", type=Path, help="Output PDF path")
    p_merge.add_argument("inputs", type=Path, nargs="+", help="Input PDF files")

    p_split = subparsers.add_parser("split", help="Export selected pages to a new PDF")
    p_split.add_argument("input", type=Path, help="Input PDF path")
    p_split.add_argument("output", type=Path, help="Output PDF path")
    p_split.add_argument("pages", help='Pages to export (e.g. "1,3,5-7")')

    p_rotate = subparsers.add_parser("rotate", help="Rotate pages")
    p_rotate.add_argument("input", type=Path, help="Input PDF path")
    p_rotate.add_argument("output", type=Path, help="Output PDF path")
    p_rotate.add_argument("angle", type=int, help="Rotation angle (must be multiple of 90)")
    p_rotate.add_argument("--pages", help='Optional page list (e.g. "1,3,5-7"). Defaults to all pages.')

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "extract-text":
        text = extract_text(args.input, args.output)
        if args.output is None:
            print(text)
    elif args.command == "merge":
        merge_pdfs(args.inputs, args.output)
    elif args.command == "split":
        split_pdf(args.input, args.output, _parse_pages(args.pages))
    elif args.command == "rotate":
        pages = _parse_pages(args.pages) if args.pages else None
        rotate_pdf(args.input, args.output, args.angle, pages)
    else:
        parser.error(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
