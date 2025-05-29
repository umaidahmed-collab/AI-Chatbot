"""
Chat router.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import json

from app.models.database import User
from app.models.schemas import (
    ChatRequest, 
    ChatResponse, 
    ChatSession as ChatSessionSchema,
    ChatMessage as ChatMessageSchema
)
from app.services.auth import get_current_active_user
from app.services.database import get_db
from app.services.chat_service import chat_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Send a chat message and get AI response."""
    try:
        response = await chat_service.generate_response(db, request, current_user)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.get("/sessions", response_model=List[ChatSessionSchema])
async def get_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's chat sessions."""
    sessions = chat_service.get_user_sessions(db, current_user)
    return sessions


@router.get("/sessions/{session_id}", response_model=ChatSessionSchema)
async def get_chat_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get chat session by ID."""
    session = chat_service.get_session(db, session_id, current_user)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageSchema])
async def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get messages for a chat session."""
    session = chat_service.get_session(db, session_id, current_user)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = chat_service.get_session_messages(db, session_id)
    return messages


@router.post("/sessions", response_model=ChatSessionSchema)
async def create_chat_session(
    title: str = "New Chat",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new chat session."""
    session = chat_service.create_session(db, current_user, title)
    return session


# WebSocket endpoint for real-time chat
@router.websocket("/ws/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: int,
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # For simplicity, we'll skip authentication in WebSocket
            # In production, you should implement proper WebSocket authentication
            
            # Process message (this is a simplified version)
            response_text = f"Echo: {message_data.get('message', '')}"
            
            # Send response back to client
            await websocket.send_text(json.dumps({
                "message": response_text,
                "timestamp": "2024-01-01T00:00:00Z"
            }))
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
