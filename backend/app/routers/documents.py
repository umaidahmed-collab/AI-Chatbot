"""
Documents router.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session

from app.models.database import User, Document as DocumentModel
from app.models.schemas import Document as DocumentSchema
from app.services.auth import get_current_active_user
from app.services.database import get_db
from app.services.document_processor import document_processor

router = APIRouter()


async def process_document_background(file_path: str, document_id: int, db: Session):
    """Background task to process document."""
    try:
        success = await document_processor.process_document(file_path, document_id)

        # Update document status in database
        document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
        if document:
            document.processed = success
            db.commit()

        if success:
            print(f"Document {document_id} processed successfully")
        else:
            print(f"Failed to process document {document_id}")
    except Exception as e:
        print(f"Error in background processing for document {document_id}: {e}")
        # Mark as failed in database
        document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
        if document:
            document.processed = False
            db.commit()


@router.post("/upload", response_model=DocumentSchema)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a document."""
    # Save file
    file_path, unique_filename = await document_processor.save_file(file)
    
    # Create document record
    document = DocumentModel(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file.size,
        content_type=file.content_type,
        owner_id=current_user.id
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Process document in background
    background_tasks.add_task(process_document_background, file_path, document.id, db)
    
    return document


@router.get("/", response_model=List[DocumentSchema])
async def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's documents."""
    documents = db.query(DocumentModel).filter(
        DocumentModel.owner_id == current_user.id
    ).all()
    return documents


@router.get("/{document_id}", response_model=DocumentSchema)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get document by ID."""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete document."""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete chunks from ChromaDB
    try:
        document_processor.delete_document_chunks(document_id)
    except Exception as e:
        print(f"Warning: Failed to delete document chunks from ChromaDB: {e}")

    # Delete file from disk
    import os
    if os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            print(f"Warning: Failed to delete file from disk: {e}")

    # Delete from database
    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}


@router.get("/stats")
async def get_document_stats(
    current_user: User = Depends(get_current_active_user)
):
    """Get document processing statistics."""
    try:
        stats = document_processor.get_document_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")
