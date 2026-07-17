# pdf-extract — Skill Card

| Field | Value |
|-------|-------|
| **Name** | pdf-extract |
| **Version** | — |
| **One-liner** | Extract text, tables, and structured content from PDF files. |

## Trigger
- "Extract text from this PDF"
- "Read/analyze/summarize this PDF"
- "What's in this PDF?"

## Key Commands

```bash
cd ~/.openclaw/workspace/pdf-tools
source bin/activate 2>/dev/null || true

# Extract all text (best for tables/structure)
./pdf_extract.py /path/to/file.pdf

# Extract specific pages
./pdf_extract.py /path/to/file.pdf --pages 1,3-5

# Fast extraction (best for speed)
./pdf_extract.py /path/to/file.pdf --method pymupdf

# Pipe for quick checks
./pdf_extract.py paper.pdf --pages 1 | head -50
```

## Dependencies
- Python 3, virtualenv at `~/.openclaw/workspace/pdf-tools/`
- `pdfplumber` (default, excellent tables) or `pymupdf` (fast)

## Quick Example

```bash
./pdf_extract.py research-paper.pdf --pages 1-3 > /tmp/extracted.txt
```

> For scanned PDFs (no text layer), use OCR tools instead.
