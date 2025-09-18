"""
Chat service for handling conversations and AI responses.
"""

from openai import AsyncOpenAI
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.database import ChatSession, ChatMessage, User
from app.models.schemas import ChatRequest, ChatResponse
from app.services.document_processor import document_processor
from app.utils.config import settings


class ChatService:
    """Chat service for managing conversations."""
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY if settings.OPENAI_API_KEY else None
        )
        self.model = "gpt-3.5-turbo"
    
    def create_session(self, db: Session, user: User, title: Optional[str] = None) -> ChatSession:
        """Create a new chat session."""
        session = ChatSession(
            user_id=user.id,
            title=title or "New Chat"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    def get_session(self, db: Session, session_id: int, user: User) -> Optional[ChatSession]:
        """Get a chat session by ID."""
        return db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user.id
        ).first()
    
    def get_user_sessions(self, db: Session, user: User) -> List[ChatSession]:
        """Get all chat sessions for a user."""
        return db.query(ChatSession).filter(
            ChatSession.user_id == user.id
        ).order_by(ChatSession.updated_at.desc()).all()
    
    def add_message(
        self, 
        db: Session, 
        session_id: int, 
        content: str, 
        role: str
    ) -> ChatMessage:
        """Add a message to a chat session."""
        message = ChatMessage(
            session_id=session_id,
            content=content,
            role=role
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def get_session_messages(self, db: Session, session_id: int) -> List[ChatMessage]:
        """Get all messages for a session."""
        return db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.timestamp.asc()).all()
    
    async def generate_response(
        self,
        db: Session,
        request: ChatRequest,
        user: User
    ) -> ChatResponse:
        """Generate AI response to user message."""
        # Get or create session
        if request.session_id:
            session = self.get_session(db, request.session_id, user)
            if not session:
                raise ValueError("Session not found")
        else:
            session = self.create_session(db, user)
        
        # Add user message
        self.add_message(db, session.id, request.message, "user")
        
        # Get context from documents if requested
        context = ""
        sources = []
        if request.use_documents:
            doc_results = document_processor.search_documents(request.message)
            if doc_results:
                context = "\n\n".join([result["content"] for result in doc_results])
                sources = [f"Document {result['metadata']['document_id']}" for result in doc_results]
        
        # Get conversation history
        messages = self.get_session_messages(db, session.id)
        conversation_history = []
        for msg in messages[-10:]:  # Last 10 messages
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Generate AI response
        ai_response = await self._call_openai(
            request.message,
            context,
            conversation_history
        )
        
        # Add AI response
        self.add_message(db, session.id, ai_response, "assistant")
        
        return ChatResponse(
            message=ai_response,
            session_id=session.id,
            sources=sources if sources else None
        )
    
    async def _call_openai(
        self,
        user_message: str,
        context: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Call OpenAI API to generate response."""
        if not settings.OPENAI_API_KEY:
            return self._fallback_response(user_message, context)
        
        try:
            # Prepare system message
            system_message = "You are a helpful AI assistant."
            if context:
                system_message += f"\n\nUse the following context to answer questions:\n{context}"
            
            # Prepare messages
            messages = [{"role": "system", "content": system_message}]
            messages.extend(conversation_history[:-1])  # Exclude the last user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content
        
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_response(user_message, context)
    
    def _fallback_response(self, user_message: str, context: str) -> str:
        """Fallback response when OpenAI is not available."""
        if context:
            return f"Based on the uploaded documents, I found some relevant information. However, I need an OpenAI API key to provide a detailed response. Your question was: {user_message}"
        else:
            return f"I received your message: '{user_message}'. However, I need an OpenAI API key to provide intelligent responses. Please configure the OPENAI_API_KEY environment variable."


# Global instance
chat_service = ChatService()
