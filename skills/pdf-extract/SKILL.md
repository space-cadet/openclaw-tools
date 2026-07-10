---
name: pdf-extract
description: "Extract text, tables, and structured content from PDF files using pdfplumber or PyMuPDF. More capable than summarize.sh for PDFs — supports page selection, structured layout extraction, and fine-grained control. Use when the user needs to extract, search, or analyze content from PDF files."
metadata:
  openclaw:
    emoji: "📄"
    requires:
      bins: ["python3"]
    install: []
---

# PDF Extract

Fast, structured PDF text extraction. Superior to summarize.sh for PDFs because it:
- Supports **page selection** (`--pages 1,3-5`)
- Uses **pdfplumber** for structured layouts and tables (default)
- Uses **PyMuPDF** for fast raw text extraction
- Outputs clean, page-delimited text suitable for analysis

## When to use

Use this skill immediately when the user asks any of:
- "extract text from this PDF"
- "read/analyze/summarize this PDF file"
- "what's in this PDF?"
- "get content from these PDF pages"
- Any task involving local PDF file analysis

## Quick start

```bash
cd ~/.openclaw/workspace/pdf-tools
source bin/activate 2>/dev/null || true

# Extract all text (pdfplumber - best for tables/structure)
./pdf_extract.py /path/to/file.pdf

# Extract specific pages
./pdf_extract.py /path/to/file.pdf --pages 1,3-5

# Fast extraction (PyMuPDF - best for speed/simple text)
./pdf_extract.py /path/to/file.pdf --method pymupdf

# Combine: fast extract of specific pages
./pdf_extract.py /path/to/file.pdf --method pymupdf --pages 1-10
```

## Methods

| Method | Best for | Speed | Table support |
|--------|---------|-------|---------------|
| `pdfplumber` (default) | Structured docs, tables, forms | Medium | Excellent |
| `pymupdf` | Raw text, speed, large files | Fast | Basic |

## Page selection syntax

- `--pages 1` — page 1 only
- `--pages 1,3,5` — specific pages
- `--pages 1-5` — range (inclusive)
- `--pages 1,3-5,10` — mixed

## Integration with LLM analysis

Extract first, then analyze:

```bash
# Extract to file for further processing
./pdf_extract.py paper.pdf --pages 1-3 > /tmp/extracted.txt
# Then read the file and ask questions about it
```

Or pipe directly for quick checks:

```bash
./pdf_extract.py paper.pdf --pages 1 | head -50
```

## Error handling

- **File not found**: Check path, try absolute path
- **Empty output**: PDF may be scanned image (no text layer) — use OCR tools instead
- **Import errors**: Ensure virtualenv is activated: `source ~/.openclaw/workspace/pdf-tools/bin/activate`

## Dependencies

Located in `~/.openclaw/workspace/pdf-tools/`:
- `pdfplumber` — Python PDF parsing
- `pymupdf` (fitz) — Fast PDF rendering
- Virtual environment pre-configured

## Compared to summarize.sh

| | `pdf_extract.py` | `summarize` |
|---|---|---|
| **PDF-specific** | Yes — purpose-built | Generic (URL/file) |
| **Page selection** | ✅ Native `--pages` | ❌ No |
| **Table extraction** | ✅ Excellent (pdfplumber) | ❌ Plain text only |
| **Structured output** | ✅ Page-delimited | ❌ Wall of text |
| **LLM summary** | ❌ Extraction only | ✅ Built-in |
| **Best use case** | Precise extraction → then analyze | Quick one-liner summary |

**Workflow**: Use `pdf_extract.py` to extract precisely what you need, then use the model directly for analysis/summarization.
