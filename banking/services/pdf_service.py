from pypdf import PdfReader
from pypdf.errors import PdfReadError


class PDFExtractionError(Exception):
    """Raised when text cannot be extracted from an uploaded PDF."""


def extract_text_from_pdf(file) -> str:
    """
    Extract text from a text-based PDF file-like object.

    Returns the concatenated page text. Raises PDFExtractionError if the file
    is not a readable PDF or contains no extractable text (e.g. a scanned /
    image-only document that would require OCR).
    """
    try:
        reader = PdfReader(file)
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
    except (PdfReadError, Exception) as exc:  # pragma: no cover - defensive
        raise PDFExtractionError(f"Could not read PDF: {exc}") from exc

    text = "\n\n".join(part for part in pages if part).strip()

    if not text:
        raise PDFExtractionError(
            "No text could be extracted. The PDF may be scanned or image-only, "
            "which would require OCR. Paste the content manually instead."
        )

    return text
