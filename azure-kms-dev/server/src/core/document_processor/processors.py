from abc import ABC, abstractmethod
from pathlib import Path
import asyncio
import aiofiles
import docx2txt
from pypdf import PdfReader
from typing import Dict, Type

from .schemas import Document
from src.api.chat.models import FileType


class BaseDocumentProcessor(ABC):
    @abstractmethod
    async def extract_text(self, temp_file_path: Path) -> Document:
        """Extract text from the given file path."""
        pass


class TXTProcessor(BaseDocumentProcessor):
    async def extract_text(self, temp_file_path: Path) -> Document:
        """Extract text from a TXT file."""
        try:
            async with aiofiles.open(temp_file_path, 'r', encoding='utf-8') as f:
                content = await f.read()

            if not content.strip():
                raise ValueError("TXT file is empty or contains only whitespace")

            return Document(
                name=temp_file_path.name,
                content=content.strip()
            )
        except Exception as e:
            raise RuntimeError(f"Failed to process TXT file: {e}")


class DOCXProcessor(BaseDocumentProcessor):
    async def extract_text(self, temp_file_path: Path) -> Document:
        """Extract text from a DOCX file using docx2txt."""
        try:
            content = await asyncio.to_thread(
                docx2txt.process,
                str(temp_file_path),
            )

            if not content or not content.strip():
                raise ValueError("DOCX file is empty or contains no extractable text")

            return Document(
                name=temp_file_path.name,
                content=content.strip()
            )
        except Exception as e:
            raise RuntimeError(f"Failed to process DOCX file: {e}")


class PDFProcessor(BaseDocumentProcessor):
    async def extract_text(self, temp_file_path: Path) -> Document:
        """Extract text from a PDF file using pypdf."""
        try:
            # Run PDF processing in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(
                None,
                self._extract_pdf_text,
                temp_file_path
            )

            if not content or not content.strip():
                raise ValueError("PDF file is empty or contains no extractable text")

            return Document(
                name=temp_file_path.name,
                content=content.strip()
            )
        except Exception as e:
            raise RuntimeError(f"Failed to process PDF file: {e}")

    def _extract_pdf_text(self, temp_file_path: Path) -> str:
        """Synchronous PDF text extraction helper."""
        with open(temp_file_path, 'rb') as file:
            pdf_reader = PdfReader(file)

            if len(pdf_reader.pages) == 0:
                raise ValueError("PDF file has no pages")

            text_content = []
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content.append(page_text)
                except Exception:
                    continue

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