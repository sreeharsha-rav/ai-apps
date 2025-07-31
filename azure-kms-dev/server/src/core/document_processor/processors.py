from abc import ABC, abstractmethod
from io import BytesIO
import asyncio
import docx2txt
import fitz
from typing import Dict, Type

from src.api.chat.models import FileType


class BaseDocumentProcessor(ABC):
    @abstractmethod
    async def extract_text(self, filename: str, file_bytes: BytesIO) -> str:
        """Extract text from given file stream."""
        pass


class TXTProcessor(BaseDocumentProcessor):
    async def extract_text(self, filename: str, file_bytes: BytesIO) -> str:
        """Extract text from a TXT file stream."""
        try:
            file_bytes.seek(0)
            content = file_bytes.read().decode('utf-8')

            if not content.strip():
                raise ValueError("TXT file is empty or contains only whitespace")

            return content.strip()
        except UnicodeDecodeError as e:
            raise RuntimeError(f"Failed to decode TXT file - invalid UTF-8 encoding: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to process TXT file: {e}")

class DOCXProcessor(BaseDocumentProcessor):
    async def extract_text(self, filename: str, file_bytes: BytesIO) -> str:
        """Extract text from a DOCX file stream using docx2txt."""
        try:
            file_bytes.seek(0)
            content = await asyncio.to_thread(docx2txt.process, file_bytes)

            if not content or not content.strip():
                raise ValueError("DOCX file is empty or contains no extractable text")

            return content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to process DOCX file: {e}")


class PDFProcessor(BaseDocumentProcessor):
    async def extract_text(self, filename: str, file_bytes: BytesIO) -> str:
        """Extract text from a PDF file using pypdf."""
        try:
            # Run PDF processing in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(
                None,
                self._extract_pdf_text,
                file_bytes
            )

            if not content or not content.strip():
                raise ValueError("PDF file is empty or contains no extractable text")

            return content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to process PDF file: {e}")

    def _extract_pdf_text(self, file_bytes: BytesIO) -> str:
        """Synchronous PDF text extraction helper."""
        text_content = []
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text and page_text.strip():
                    text_content.append(page_text)
        if not text_content:
            raise ValueError("No text content could be extracted from PDF")
        return '\n\n'.join(text_content)


class DocumentProcessorFactory:
    """Factory class to create document processors based on file extension."""

    _processors: Dict[FileType, Type[BaseDocumentProcessor]] = {
        FileType.TXT: TXTProcessor,
        FileType.DOCX: DOCXProcessor,
        FileType.PDF: PDFProcessor,
    }

    @classmethod
    def get_processor(cls, file_extension: FileType) -> BaseDocumentProcessor:
        """Get the appropriate document processor for the given file extension."""
        if file_extension not in cls._processors:
            raise ValueError(f"No processor available for file extension: {file_extension}")
        processor_class = cls._processors[file_extension]
        return processor_class()