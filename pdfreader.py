from pathlib import Path
import argparse
import sys

import fitz  # PyMuPDF


def read_pdf_text(pdf_path: str | Path) -> str:
    """
    Read all text from a PDF file using PyMuPDF.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path}")

    text_chunks: list[str] = []
    with fitz.open(path) as doc:
        for page in doc:
            text_chunks.append(page.get_text())
    return "\n".join(text_chunks).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Read text from a PDF using PyMuPDF.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    args = parser.parse_args()

    try:
        text = read_pdf_text(args.pdf_path)
        print(text)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
