import io
import re
from typing import Tuple
import pymupdf  # PyMuPDF
import docx  # python-docx


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class DocumentParserError(Exception):
    pass


class DocumentParser:
    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
        """
        Extract clean text from PDF or DOCX file bytes.
        """
        if not file_bytes:
            raise DocumentParserError("Uploaded file is empty.")

        if len(file_bytes) > MAX_FILE_SIZE:
            raise DocumentParserError("File size exceeds 10MB limit.")

        filename_lower = filename.lower()
        if filename_lower.endswith(".pdf"):
            return DocumentParser._extract_from_pdf(file_bytes)
        elif filename_lower.endswith(".docx"):
            return DocumentParser._extract_from_docx(file_bytes)
        else:
            raise DocumentParserError("Unsupported file type. Please upload a .pdf or .docx file.")

    @staticmethod
    def _extract_from_pdf(file_bytes: bytes) -> str:
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            if doc.page_count == 0:
                raise DocumentParserError("PDF file has no pages.")
            
            text_parts = []
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                page_text = page.get_text("text")
                if page_text:
                    text_parts.append(page_text)
            
            doc.close()
            full_text = "\n".join(text_parts).strip()
            if not full_text:
                raise DocumentParserError("Could not extract any readable text from the PDF. It may be scanned or image-only.")
            return full_text
        except Exception as e:
            if isinstance(e, DocumentParserError):
                raise
            raise DocumentParserError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def _extract_from_docx(file_bytes: bytes) -> str:
        try:
            doc_file = io.BytesIO(file_bytes)
            doc = docx.Document(doc_file)
            
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                    if row_text:
                        paragraphs.append(row_text)
            
            full_text = "\n".join(paragraphs).strip()
            if not full_text:
                raise DocumentParserError("Could not extract any readable text from the DOCX file.")
            return full_text
        except Exception as e:
            if isinstance(e, DocumentParserError):
                raise
            raise DocumentParserError(f"Failed to parse DOCX: {str(e)}")
