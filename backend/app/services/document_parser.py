from io import BytesIO
from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file_content: bytes) -> str:
    """Extract text from a PDF file."""
    pdf_file = BytesIO(file_content)
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_docx_text(file_content: bytes) -> str:
    """Extract text from a DOCX file."""
    docx_file = BytesIO(file_content)
    document = Document(docx_file)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text.strip()


def extract_resume_text(filename: str, file_content: bytes) -> str:
    """Detect file type and extract text."""

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file_content)

    elif filename.endswith(".docx"):
        return extract_docx_text(file_content)

    else:
        raise ValueError("Only PDF and DOCX files are supported.")
    