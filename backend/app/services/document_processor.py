"""
Document processing service for extracting text and creating embeddings.
"""

import os
import uuid
from typing import List, Optional
from pathlib import Path
import aiofiles
from fastapi import UploadFile, HTTPException

# Document processing imports
import PyPDF2
from docx import Document as DocxDocument
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from app.utils.config import settings


class DocumentProcessor:
    """Document processing service."""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    async def save_file(self, file: UploadFile) -> tuple[str, str]:
        """Save uploaded file to disk."""
        # Validate file type
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not allowed"
            )
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = self.upload_dir / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail="File too large"
                )
            await f.write(content)
        
        return str(file_path), unique_filename
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from document."""
        file_extension = Path(file_path).suffix.lower()
        
        try:
            if file_extension == '.pdf':
                return self._extract_pdf_text(file_path)
            elif file_extension == '.docx':
                return self._extract_docx_text(file_path)
            elif file_extension == '.txt':
                return self._extract_txt_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting text: {str(e)}"
            )
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = DocxDocument(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    async def process_document(self, file_path: str, document_id: int) -> bool:
        """Process document and store embeddings."""
        try:
            # Extract text
            text = self.extract_text(file_path)
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Create embeddings and store in ChromaDB
            for i, chunk in enumerate(chunks):
                chunk_id = f"doc_{document_id}_chunk_{i}"
                embedding = self.embeddings.embed_query(chunk)
                
                self.collection.add(
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        "document_id": document_id,
                        "chunk_index": i,
                        "file_path": file_path
                    }],
                    ids=[chunk_id]
                )
            
            return True
        except Exception as e:
            print(f"Error processing document: {e}")
            return False
    
    def search_documents(self, query: str, n_results: int = 5) -> List[dict]:
        """Search for relevant document chunks."""
        try:
            query_embedding = self.embeddings.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            return [
                {
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []


# Global instance
document_processor = DocumentProcessor()
